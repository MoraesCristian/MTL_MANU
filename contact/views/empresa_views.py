from django.shortcuts import render
from contact.models import Empresa
from django.contrib.auth.decorators import login_required

@login_required
def empresas_view(request):
    empresas = Empresa.objects.all()  # Obtém todas as empresas
    return render(request, 'contact/empresas.html', {'empresas': empresas})

