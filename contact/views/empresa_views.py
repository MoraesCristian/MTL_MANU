from django.shortcuts import render, redirect, get_object_or_404
from contact.models import Empresa
from django.contrib.auth.decorators import login_required, user_passes_test
from contact.forms.empresa_forms import AdicionarEmpresaForm, EmpresaForm

def is_admin(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(is_admin)
@login_required
def empresas_view(request):
    empresas = Empresa.objects.all()  # Obtém todas as empresas
    return render(request, 'contact/empresas.html', {'empresas': empresas})

@user_passes_test(is_admin)
@login_required
def empresa_detalhes_view(request, empresa_id):
    empresa = get_object_or_404(Empresa, id=empresa_id)
    return render(request, 'contact/empresas_details.html', {'empresa': empresa})

@user_passes_test(is_admin)
@login_required
def adicionar_empresa_view(request):
    if request.method == 'POST':
        form = AdicionarEmpresaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact:empresas_view')
    else:
        form = AdicionarEmpresaForm()
    return render(request, 'contact/adicionar_empresa.html', {'form': form})

@user_passes_test(is_admin)
@login_required
def editar_empresa_view(request, empresa_id):
    empresa = get_object_or_404(Empresa, id=empresa_id)
    if request.method == 'POST':
        form = EmpresaForm(request.POST, instance=empresa)
        if form.is_valid():
            form.save()
            return redirect('contact:empresas_details', empresa_id=empresa.id)
    else:
        form = EmpresaForm(instance=empresa)
    return render(request, 'contact/edit_empresas.html', {'form': form, 'empresa': empresa})
