from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from contact.models import Chamado, Chat, MensagemChat
from contact.forms.chamado_forms import MensagemChatForm
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
    # Lógica para carregar as tarefas
    context = {
        'tarefas': 'Tarefas a realizar'  # Substitua pelo conteúdo real
    }
    return render(request, 'contact/tarefas_a_realizar.html', context)
