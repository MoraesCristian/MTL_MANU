from django.shortcuts import render
from contact.models import Chamado
from django.contrib.auth.decorators import login_required

@login_required
def chamados_view(request):
    chamados = Chamado.objects.all()  # Obtém todos os chamados
    return render(request, 'contact/chamados.html', {'chamados': chamados})