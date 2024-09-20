from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from contact.models import Chamado

@login_required
def visualizar_chamado(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)
    context = {
        'chamado': chamado,
    }
    return render(request, 'contact/visualizar_chamado.html', context)

@login_required
def load_chat(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)
    # Lógica para carregar o chat
    context = {
        'chat': 'Conteúdo do chat'  # Substitua pelo conteúdo real
    }
    return render(request, 'contact/chat.html', context)

@login_required
def load_informacao_chamado(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)
    # Lógica para carregar as informações do chamado
    context = {
        'informacao_chamado': 'Informações do chamado'  # Substitua pelo conteúdo real
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

