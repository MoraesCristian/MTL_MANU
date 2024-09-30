from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from contact.models import Chamado, Chat, MensagemChat, Tarefa,DetalheTarefa, DetalheTarefaPreenchido
from contact.forms.chamado_forms import MensagemChatForm
from contact.forms.tarefa_forms import DetalheTarefaPreenchidoForm
from django.http import JsonResponse

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
            mensagem = MensagemChat.objects.create(chat=chat, usuario=request.user, conteudo=mensagem_texto)
            return JsonResponse({
                'usuario': {
                    'first_name': mensagem.usuario.first_name,
                    'last_name': mensagem.usuario.last_name
                },
                'conteudo': mensagem.conteudo,
                'data_envio': mensagem.data_envio.strftime('%Y-%m-%d %H:%M:%S')
            })
    
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


@login_required
def load_tarefas_a_realizar(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)
    tarefas = Tarefa.objects.filter(area=chamado.area_chamado)  # Filtrar tarefas pela área do chamado
    detalhes_tarefas = DetalheTarefa.objects.filter(tarefa__in=tarefas)  # Filtrar detalhes pelas tarefas

    context = {
        'tarefas': tarefas,
        'detalhes_tarefas': detalhes_tarefas,
        'chamado': chamado,
    }
    return render(request, 'contact/tarefas_a_realizar.html', context)

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
    detalhe_preenchido = get_object_or_404(DetalheTarefaPreenchido, detalhe_tarefa=detalhe_tarefa, chamado=chamado)

    print(request.method)
    if request.method == 'POST':
        print(f'{request.method} DENTRO DO POST' )
        form = DetalheTarefaPreenchidoForm(request.POST, request.FILES, instance=detalhe_preenchido)
        if form.is_valid():
            detalhe_preenchido = form.save(commit=False)
            detalhe_preenchido.detalhe_tarefa = detalhe_tarefa
            detalhe_preenchido.chamado = chamado
            detalhe_preenchido.usuario = request.user
            detalhe_preenchido.save()
            if request.is_ajax():
                response_data = {
                    'success': True,
                    'message': 'Detalhe da tarefa atualizado com sucesso.'
                }
                return JsonResponse(response_data)
            return redirect('contact:detalhe_tarefa', chamado_id=chamado.id, tarefa_id=tarefa.id, detalhe_tarefa_id=detalhe_tarefa.id)
        else:
            if request.is_ajax():
                response_data = {
                    'success': False,
                    'errors': form.errors
                }
                return JsonResponse(response_data)
    else:
        form = DetalheTarefaPreenchidoForm(instance=detalhe_preenchido)

    context = {
        'chamado': chamado,
        'tarefa': tarefa,
        'detalhe_tarefa': detalhe_tarefa,
        'detalhe_preenchido': detalhe_preenchido,
        'form': form,
        'edit_mode': True,
        'is_new': False
    }
    return render(request, 'contact/detalhe_tarefa_form.html', context)
