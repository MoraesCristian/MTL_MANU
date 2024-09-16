from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from contact.models import Chamado, Empresa

@login_required
def listar_chamados(request):
    user = request.user
    chamados = Chamado.objects.none()  # Inicializa com um QuerySet vazio
    empresas = None

    if user.tipo_usuario == 'admin':
        empresa_filter = request.GET.get('empresa')
        chamados = Chamado.objects.all()
        if empresa_filter:
            chamados = chamados.filter(usuario__empresa__nome_fantasia=empresa_filter)
        empresas = Empresa.objects.all()

    elif user.tipo_usuario == 'manager':
        empresa_filter = request.GET.get('empresa')
        chamados = Chamado.objects.filter(usuario__empresa=user.empresa)
        if empresa_filter:
            chamados = chamados.filter(usuario__empresa__nome_fantasia=empresa_filter)
        empresas = Empresa.objects.filter(id=user.empresa.id) | Empresa.objects.filter(usuario_criador=user)

    elif user.tipo_usuario == 'tecnico':
        chamados = Chamado.objects.filter(usuario=user)

    context = {
        'chamados': chamados,
        'empresas': empresas,
        'user_tipo': user.tipo_usuario,
    }
    return render(request, 'contact/listar_chamados.html', context)