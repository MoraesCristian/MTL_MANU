from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from contact.models import Chamado, Chat, MensagemChat, Tarefa,DetalheTarefa, DetalheTarefaPreenchido,Imagem
from contact.forms.chamado_forms import MensagemChatForm
from contact.forms.tarefa_forms import DetalheTarefaPreenchidoForm
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.utils import timezone

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
            # Cria a nova mensagem
            MensagemChat.objects.create(chat=chat, usuario=request.user, conteudo=mensagem_texto)
            # Redireciona para o mesmo chat
            return redirect('contact:load_chat', chamado_id=chamado.id)
        else:
            # Se a mensagem estiver vazia, você pode optar por adicionar um erro ao contexto
            error = "Mensagem vazia."
    else:
        error = None

    mensagens = chat.mensagens.all()

    context = {
        'mensagens': mensagens,
        'chamado': chamado,
        'error': error
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
        print('if do ajax')
        return render(request, 'contact/tarefas_a_realizar.html', context)
    else:
        print('else fora do ajax')
        # Retorne uma resposta normal se não for uma requisição AJAX
        return render(request,'contact/tarefas_a_realizar.html', context)

@login_required
def detalhe_tarefa_view(request, chamado_id, tarefa_id, detalhe_tarefa_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    detalhe_tarefa = get_object_or_404(DetalheTarefa, id=detalhe_tarefa_id, tarefa=tarefa)
    detalhe_preenchido = get_object_or_404(DetalheTarefaPreenchido, detalhe_tarefa=detalhe_tarefa, chamado=chamado)

    # Supondo que o modelo Imagem tenha um campo chamado tipo que distingue entre cliente e ajuste
    imagens_clientes = chamado.imagem_set.filter(tipo_imagem='cliente')  # Filtra imagens de cliente
    imagens_ajustes = chamado.imagem_set.filter(tipo_imagem='ajuste')    # Filtra imagens de ajuste

    context = {
        'chamado': chamado,
        'tarefa': tarefa,
        'detalhe_tarefa': detalhe_tarefa,
        'detalhe_preenchido': detalhe_preenchido,
        'imagens_clientes': imagens_clientes,  # Adiciona as imagens de clientes ao contexto
        'imagens_ajustes': imagens_ajustes,      # Adiciona as imagens de ajustes ao contexto
        'edit_mode': False,
    }
    return render(request, 'contact/detalhe_tarefa.html', context)


@login_required
def detalhe_tarefa_edit_view(request, chamado_id, tarefa_id, detalhe_tarefa_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    detalhe_tarefa = get_object_or_404(DetalheTarefa, id=detalhe_tarefa_id, tarefa=tarefa)

    if chamado.status_chamado == 'concluido' and request.user.tipo_usuario not in ['admin', 'operador']:
        raise PermissionDenied("Você não tem permissão para editar este chamado.")

    try:
        detalhe_preenchido = DetalheTarefaPreenchido.objects.get(detalhe_tarefa=detalhe_tarefa, chamado=chamado)
        imagens_clientes = detalhe_preenchido.imagens.filter(tipo_imagem='cliente')
        imagens_ajustes = detalhe_preenchido.imagens.filter(tipo_imagem='ajuste')
    except DetalheTarefaPreenchido.DoesNotExist:
        detalhe_preenchido = None
        imagens_clientes = []
        imagens_ajustes = []

    if request.method == 'POST':
        if 'excluir_imagem' in request.POST:
            imagem_id = request.POST.get('imagem_id')
            try:
                imagem = Imagem.objects.get(id=imagem_id)
                imagem.delete()
            except Imagem.DoesNotExist:
                pass  # Imagem não existe, não faz nada

            return redirect('contact:detalhe_tarefa', chamado.id, tarefa.id, detalhe_tarefa.id)

        form = DetalheTarefaPreenchidoForm(request.POST, request.FILES, instance=detalhe_preenchido)
        if form.is_valid():
            detalhe_preenchido = form.save(commit=False)
            detalhe_preenchido.detalhe_tarefa = detalhe_tarefa
            detalhe_preenchido.chamado = chamado
            detalhe_preenchido.usuario = request.user
            detalhe_preenchido.save()

            # Salvar imagens aqui...

            return redirect('contact:detalhe_tarefa', chamado.id, tarefa.id, detalhe_tarefa.id)
    else:
        form = DetalheTarefaPreenchidoForm(instance=detalhe_preenchido)

    context = {
        'form': form,
        'detalhe_preenchido': detalhe_preenchido,
        'imagens_clientes': imagens_clientes,
        'imagens_ajustes': imagens_ajustes,
    }
    return render(request, 'contact/detalhe_tarefa_form.html', context)


@login_required
def atualizar_status_chamado_view(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)

    if request.method == 'POST':
        novo_status = request.POST.get('status_chamado')
        print(f"Recebido novo status: {novo_status}")

        if novo_status not in ['aberto', 'executando', 'concluido', 'rejeitado']:
            return redirect('contact:listar_chamados')

        redirection_url = 'contact:listar_chamados'
        redirection_args = {}

        if request.user.is_staff or request.user.tipo_usuario == 'operador':
            chamado.status_chamado = novo_status

            if novo_status == 'aberto':
                redirection_url = 'contact:visualizar_chamado'
                redirection_args = {'chamado_id': chamado.id}
            elif novo_status == 'executando':
                chamado.data_inicio_atv = timezone.now()
                redirection_url = 'contact:visualizar_chamado'
                redirection_args = {'chamado_id': chamado.id}
            elif novo_status == 'concluido':
                chamado.data_fim_atv = timezone.now()
            elif novo_status == 'rejeitado':
                redirection_url = 'contact:listar_chamados'

            chamado.save()
            return redirect(redirection_url, **redirection_args)

        elif request.user.is_authenticated:
            if chamado.prestadora_servico == request.user.empresa:
                if novo_status in ['executando', 'concluido']:
                    chamado.status_chamado = novo_status
                    
                    if novo_status == 'executando':
                        chamado.data_inicio_atv = timezone.now()
                        redirection_url = 'contact:visualizar_chamado'
                        redirection_args = {'chamado_id': chamado.id}
                    elif novo_status == 'concluido':
                        chamado.data_fim_atv = timezone.now()
                        redirection_url = 'contact:listar_chamados'

                    chamado.save()
                    return redirect(redirection_url, **redirection_args)

        return redirect('contact:listar_chamados')

    context = {
        'chamado': chamado,
    }
    return render(request, 'contact/visualizar_chamado.html', context)


