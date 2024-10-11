from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from contact.models import Chamado, Chat, MensagemChat, Tarefa,DetalheTarefa, DetalheTarefaPreenchido,Imagem
from contact.forms.chamado_forms import MensagemChatForm
from contact.forms.tarefa_forms import DetalheTarefaPreenchidoForm
from django.http import JsonResponse
from django.urls import reverse

@login_required
def visualizar_chamado(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)
    chat, created = Chat.objects.get_or_create(chamado=chamado)
    mensagens = chat.mensagens.all()

    if request.method == 'POST':
        form = MensagemChatForm(request.POST)
        if form.is_valid():
            mensagem = form.save(commit=False)
            mensagem.chat = chat
            mensagem.usuario = request.user
            mensagem.save()
            return redirect('contact:visualizar_chamado', chamado_id=chamado.id)
    else:
        form = MensagemChatForm()

    print(f"Visualizando chamado: {chamado.id}, Status: {chamado.status_chamado}")
    context = {
        'chamado': chamado,
        'chat': chat,
        'mensagens': mensagens,
        'form': form
    }
    return render(request, 'contact/visualizar_chamado.html', context)


@login_required
def load_chat(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)
    chat, created = Chat.objects.get_or_create(chamado=chamado)
    
    if request.method == 'POST':
        mensagem_texto = request.POST.get('mensagem')
        if mensagem_texto:
            mensagem = MensagemChat.objects.create(chat=chat, usuario=request.user, conteudo=mensagem_texto)
            return JsonResponse({
                'success': True,
                'usuario': {
                    'first_name': mensagem.usuario.first_name,
                    'last_name': mensagem.usuario.last_name
                },
                'conteudo': mensagem.conteudo,
                'data_envio': mensagem.data_envio.strftime('%Y-%m-%d %H:%M:%S')
            })
        else:
            return JsonResponse({'success': False, 'error': 'Mensagem vazia'}, status=400)
    
    mensagens = chat.mensagens.all()
    
    context = {
        'mensagens': mensagens,
        'chamado': chamado
    }
    return render(request, 'contact/chat.html', context)

@login_required
def load_informacao_chamado(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)
    context = {
        'chamado': chamado,
        'empresa': chamado.empresa,
        'prestadora_servico': chamado.prestadora_servico,
        'tecnico_responsavel': chamado.tecnico_responsavel,
    }
    return render(request, 'contact/informacao_chamado.html', context)

# @login_required
# def load_tarefas_a_realizar(request, chamado_id):
#     chamado = get_object_or_404(Chamado, id=chamado_id)
#     tarefas = Tarefa.objects.filter(area=chamado.area_chamado)  # Filtrar tarefas pela área do chamado
#     detalhes_tarefas = DetalheTarefa.objects.filter(tarefa__in=tarefas)  # Filtrar detalhes pelas tarefas

#     context = {
#         'tarefas': tarefas,
#         'detalhes_tarefas': detalhes_tarefas,
#         'chamado': chamado,
#     }
#     return render(request, 'contact/tarefas_a_realizar.html', context)

@login_required
def load_tarefas_a_realizar(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)
    tarefas = Tarefa.objects.filter(area=chamado.area_chamado)
    detalhes_tarefas = DetalheTarefa.objects.filter(tarefa__in=tarefas)

    context = {
        'chamado': chamado,
        'tarefas': tarefas,
        'detalhes_tarefas': detalhes_tarefas
    }

    # Verifique se a requisição é AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'contact/tarefas_a_realizar.html', context)
    else:
        # Retorne uma resposta normal se não for uma requisição AJAX
        return render(request,'contact/tarefas_a_realizar.html', context)


@login_required
def detalhe_tarefa_view(request, chamado_id, tarefa_id, detalhe_tarefa_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    detalhe_tarefa = get_object_or_404(DetalheTarefa, id=detalhe_tarefa_id, tarefa=tarefa)
    detalhe_preenchido = get_object_or_404(DetalheTarefaPreenchido, detalhe_tarefa=detalhe_tarefa, chamado=chamado)

    context = {
        'chamado': chamado,
        'tarefa': tarefa,
        'detalhe_tarefa': detalhe_tarefa,
        'detalhe_preenchido': detalhe_preenchido,
        'edit_mode': False,
    }
    return render(request, 'contact/detalhe_tarefa.html', context)



@login_required
def detalhe_tarefa_edit_view(request, chamado_id, tarefa_id, detalhe_tarefa_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    detalhe_tarefa = get_object_or_404(DetalheTarefa, id=detalhe_tarefa_id, tarefa=tarefa)

    try:
        detalhe_preenchido = DetalheTarefaPreenchido.objects.get(detalhe_tarefa=detalhe_tarefa, chamado=chamado)
        imagens_clientes = detalhe_preenchido.imagens.filter(tipo_imagem='cliente')
        imagens_ajustes = detalhe_preenchido.imagens.filter(tipo_imagem='ajuste')
    except DetalheTarefaPreenchido.DoesNotExist:
        detalhe_preenchido = None
        imagens_clientes = []
        imagens_ajustes = []

    if request.method == 'POST':
        form = DetalheTarefaPreenchidoForm(request.POST, request.FILES, instance=detalhe_preenchido)
        print("POST")
        if form.is_valid():
            print(form.is_valid())
            detalhe_preenchido = form.save(commit=False)
            detalhe_preenchido.observacao = detalhe_preenchido.observacao.strip() if detalhe_preenchido.observacao else ""
            detalhe_preenchido.detalhe_tarefa = detalhe_tarefa
            detalhe_preenchido.chamado = chamado
            detalhe_preenchido.usuario = request.user
            detalhe_preenchido.save()

            # Processamento das imagens
            contador_clientes = 1
            contador_ajustes = 1

            for imagem in request.FILES.getlist('fotos_clientes'):
                novo_nome_imagem = f"{chamado.numero_ordem}_detalhe_{detalhe_tarefa.id}_cliente_{contador_clientes}.jpg"
                imagem.name = novo_nome_imagem
                Imagem.objects.create(
                    detalhe_tarefa=detalhe_preenchido,
                    numero_ordem=chamado,
                    tarefa=tarefa,
                    imagem=imagem,
                    tipo_imagem='cliente'
                )
                contador_clientes += 1

            for imagem in request.FILES.getlist('fotos_ajustes'):
                novo_nome_imagem = f"{chamado.numero_ordem}_detalhe_{detalhe_tarefa.id}_ajuste_{contador_ajustes}.jpg"
                imagem.name = novo_nome_imagem
                Imagem.objects.create(
                    detalhe_tarefa=detalhe_preenchido,
                    numero_ordem=chamado,
                    tarefa=tarefa,
                    imagem=imagem,
                    tipo_imagem='ajuste'
                )
                contador_ajustes += 1

            # Resposta para requisições AJAX
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                print("RESPOSTA AJAX")
                response_data = {
                    'success': True,
                    'message': 'Detalhe da tarefa atualizado com sucesso.'
                }
                return JsonResponse(response_data)

        else:
            # Adicione logs para depurar erros
            print("Erros de validação do formulário:", form.errors)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                response_data = {
                    'success': False,
                    'errors': form.errors
                }
                return JsonResponse(response_data)

    else:
        print('dentro do form else')
        form = DetalheTarefaPreenchidoForm(instance=detalhe_preenchido)

        context = {
            'chamado': chamado,
            'tarefa': tarefa,
            'detalhe_tarefa': detalhe_tarefa,
            'detalhe_preenchido': detalhe_preenchido,
            'imagens_clientes': imagens_clientes,
            'imagens_ajustes': imagens_ajustes,
            'form': form,
            'edit_mode': True,
            'is_new': detalhe_preenchido is None
        }

        return render(request, 'contact/detalhe_tarefa_form.html', context)

    context = {
        'chamado': chamado,
        'tarefa': tarefa,
        'detalhe_tarefa': detalhe_tarefa
    }

    # Verifique se a requisição é AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'contact/tarefas_a_realizar.html', context)
    else:
        # Retorne uma resposta normal se não for uma requisição AJAX
        return render(request, 'contact/tarefas_a_realizar.html', context)



@login_required
def atualizar_status_chamado_view(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)

    if request.method == 'POST':
        novo_status = request.POST.get('status_chamado')
        print(f"Recebido novo status: {novo_status}")

        # Validação do novo status
        if novo_status not in ['aberto', 'executando', 'concluido', 'rejeitado']:
            print("Status inválido recebido.")
            return redirect('contact:listar_chamados')

        # Atualiza o status se o usuário for admin
        if request.user.is_staff:
            print(f"Atualizando status do chamado {chamado_id} para {novo_status} pelo admin {request.user.first_name}.")
            chamado.status_chamado = novo_status
            chamado.save()
            return redirect('contact:listar_chamados')

        # Atualiza o status se o usuário for técnico ou prestadora de serviço
        elif request.user.is_authenticated:
            # Verifica se o usuário está associado à prestadora de serviço do chamado
            if chamado.prestadora_servico == request.user.prestadora_servico:
                print(f"Atualizando status do chamado {chamado_id} para {novo_status} pelo técnico/prestadora {request.user.first_name}.")
                chamado.status_chamado = novo_status
                chamado.save()
                return redirect('contact:listar_chamados')

    print("Método não permitido ou condições não atendidas.")
    return redirect('contact:listar_chamados')
