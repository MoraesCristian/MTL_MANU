from django.shortcuts import render, redirect, get_object_or_404
from contact.models import Empresa
from django.contrib.auth.decorators import login_required, user_passes_test
from contact.forms.empresa_forms import AdicionarEmpresaForm, EmpresaForm

def is_admin(user):
    return user.is_authenticated and user.tipo_usuario == 'admin'

def is_admin_or_manager(user):
    return user.is_authenticated and (user.is_superuser or user.tipo_usuario == 'manager')


@user_passes_test(is_admin_or_manager)
@login_required
def empresas_view(request):
    user = request.user
    if user.tipo_usuario == 'admin':
        empresa_filter = request.GET.get('empresa')
        empresas = Empresa.objects.all()
        if empresa_filter:
            empresas = empresas.filter(nome_fantasia=empresa_filter)
    elif user.tipo_usuario == 'manager':
        empresa_filter = request.GET.get('empresa')
        empresas = Empresa.objects.filter(id=user.empresa_id) | Empresa.objects.filter(criado_por=user)
        if empresa_filter:
            empresas = empresas.filter(nome_fantasia=empresa_filter)
    else:
        empresas = Empresa.objects.none()

    return render(request, 'contact/empresas.html', {'empresas': empresas})


@user_passes_test(is_admin_or_manager)
@login_required
def empresa_detalhes_view(request, empresa_id):
    user = request.user
    if user.tipo_usuario == 'admin':
        empresa = get_object_or_404(Empresa, id=empresa_id)
    elif user.tipo_usuario == 'manager':
        empresa = get_object_or_404(Empresa, id=user.empresa_id)
        if empresa_id != empresa.id and empresa_id not in Empresa.objects.filter(criado_por=user).values_list('id', flat=True):
            return redirect('contact:empresas_view')
    else:
        return redirect('contact:empresas_view')

    return render(request, 'contact/empresas_details.html', {'empresa': empresa})


@user_passes_test(is_admin_or_manager)
@login_required
def adicionar_empresa_view(request):
    user = request.user
    if user.tipo_usuario != 'admin':
        return redirect('contact:empresas_view')
    
    if request.method == 'POST':
        form = AdicionarEmpresaForm(request.POST, request=request)
        form.request = request 
        if form.is_valid():
            form.save()
            return redirect('contact:empresas_view')
    else:
        form = AdicionarEmpresaForm()
    return render(request, 'contact/adicionar_empresa.html', {'form': form})


@user_passes_test(is_admin_or_manager)
@login_required
def editar_empresa_view(request, empresa_id):
    user = request.user
    if user.tipo_usuario != 'admin':
        return redirect('contact:empresas_view')
    
    empresa = get_object_or_404(Empresa, id=empresa_id)
    if request.method == 'POST':
        form = EmpresaForm(request.POST, instance=empresa)
        if form.is_valid():
            form.save()
            return redirect('contact:empresas_details', empresa_id=empresa.id)
    else:
        form = EmpresaForm(instance=empresa)
    return render(request, 'contact/edit_empresas.html', {'form': form, 'empresa': empresa})
