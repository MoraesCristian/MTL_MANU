from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from contact.models import Chamado, Empresa
from django.http import HttpResponseForbidden


@login_required
def listar_chamados(request):
    user = request.user
    chamados = Chamado.objects.none() 
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
        empresas = Empresa.objects.filter(id=user.empresa.id) | Empresa.objects.filter(criado_por=user)

    elif user.tipo_usuario == 'tecnico':
        chamados = Chamado.objects.filter(usuario=user)

    context = {
        'chamados': chamados,
        'empresas': empresas,
        'user_tipo': user.tipo_usuario,
    }
    return render(request, 'contact/listar_chamados.html', context)


@login_required
def abrir_chamado(request):
    user = request.user

    # Verifica se o usuário tem permissão para abrir chamados
    if user.tipo_usuario not in ['admin', 'cliente']:
        return HttpResponseForbidden("Você não tem permissão para acessar esta página.")

    if request.method == 'POST':
        empresa_id = request.POST.get('empresa')
        localizacao_atv = request.POST.get('localizacaoAtv')
        tipo_manutencao = request.POST.get('tipoManutencao')
        area = request.POST.get('area')
        descricao = request.POST.get('descricao')

        # Verifica se a empresa existe
        try:
            empresa = Empresa.objects.get(id=empresa_id)
        except Empresa.DoesNotExist:
            return HttpResponseForbidden("Empresa selecionada não existe.")

        # Verifica se a empresa está vinculada ao cliente
        if user.tipo_usuario == 'cliente':
            if empresa.id != user.empresa.id:
                return HttpResponseForbidden("Você não pode abrir um chamado para esta empresa.")

        chamado = Chamado(
            empresa_id=empresa_id,
            localizacao_atv=localizacao_atv,
            tipo_manutencao=tipo_manutencao,
            area=area,
            descricao=descricao,
            usuario=user
        )
        chamado.save()

        return redirect('listar_chamados')

    # Filtra empresas para exibir apenas as permitidas para o cliente
    if user.tipo_usuario == 'cliente':
        empresas = Empresa.objects.filter(id=user.empresa.id)
    else:
        empresas = Empresa.objects.all()

    return render(request, 'contact/abrir_chamado.html', {
        'empresas': empresas,
    })

