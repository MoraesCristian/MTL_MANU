from django.shortcuts import render, redirect, get_object_or_404
from contact.models import Empresa
from django.contrib.auth.decorators import login_required
from contact.forms.empresa_forms import AdicionarEmpresaForm, EmpresaForm

@login_required
def empresas_view(request):
    user = request.user
    empresas = Empresa.objects.none()

    if user.tipo_usuario in ['admin', 'operador']:
        empresas = Empresa.objects.all()
    elif user.tipo_usuario in ['manager', 'user']:
        empresas = Empresa.objects.filter(id=user.empresa_id)

    empresa_filter = request.GET.get('empresa')
    if empresa_filter:
        empresas = empresas.filter(nome_fantasia=empresa_filter)

    return render(request, 'contact/empresas.html', {'empresas': empresas})

@login_required
def empresa_detalhes_view(request, empresa_id):
    user = request.user
    if user.tipo_usuario in ['admin', 'operador']:
        empresa = get_object_or_404(Empresa, id=empresa_id)
    elif user.tipo_usuario == 'manager':
        empresa = get_object_or_404(Empresa, id=user.empresa_id)
        if empresa_id != empresa.id:
            return redirect('contact:empresas_view')
    elif user.tipo_usuario == 'user':
        empresa = get_object_or_404(Empresa, id=user.empresa_id)
        if empresa_id != empresa.id:
            return redirect('contact:empresas_view')
    else:
        return redirect('contact:empresas_view')

    return render(request, 'contact/empresas_details.html', {'empresa': empresa})

@login_required
def adicionar_empresa_view(request):
    user = request.user
    if user.tipo_usuario not in ['admin', 'operador']:
        return redirect('contact:empresas_view')

    if request.method == 'POST':
        form = AdicionarEmpresaForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            return redirect('contact:empresas_view')
    else:
        form = AdicionarEmpresaForm()
    return render(request, 'contact/adicionar_empresa.html', {'form': form})

@login_required
def editar_empresa_view(request, empresa_id):
    user = request.user
    if user.tipo_usuario not in ['admin', 'operador']:
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
