from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def cadastros_view(request):
    context = {
        'message': 'Bem-vindo à página de cadastros! Somente administradores e operadores podem ver esta página.'
    }
    return render(request, 'contact/cadastros.html', context)

