from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from contact.models import Chamado, Chat, MensagemChat, Tarefa,DetalheTarefa
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
def detalhe_tarefa_view(request, detalhe_tarefa_id):
    detalhe_tarefa = get_object_or_404(DetalheTarefa, id=detalhe_tarefa_id)
    chamado = detalhe_tarefa.tarefa.chamado  # Verifique se esta linha corresponde ao seu modelo
    if request.method == 'POST':
        form = DetalheTarefaPreenchidoForm(request.POST, request.FILES)
        if form.is_valid():
            detalhe_preenchido = form.save(commit=False)
            detalhe_preenchido.detalhe_tarefa = detalhe_tarefa
            detalhe_preenchido.chamado = chamado
            detalhe_preenchido.usuario = request.user
            detalhe_preenchido.save()
            return redirect('contact:load_tarefas_a_realizar', chamado_id=chamado.id)
    else:
        form = DetalheTarefaPreenchidoForm()

    context = {
        'detalhe_tarefa': detalhe_tarefa,
        'chamado': chamado,
        'form': form
    }
    return render(request, 'contact/detalhe_tarefa_form.html', context)
