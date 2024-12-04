from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from contact.models import Empresa, TempoManutencao, DocumentoEmpresa
from contact.forms.empresa_forms import AdicionarEmpresaForm, EmpresaForm, DocumentoForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt


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

    tempos_manutencao = TempoManutencao.objects.filter(empresa=empresa)
    documentos_financeiro = DocumentoEmpresa.objects.filter(empresa=empresa, tipo_documento='financeiro')
    documentos_contrato = DocumentoEmpresa.objects.filter(empresa=empresa, tipo_documento='contrato')

    context = {
        'empresa': empresa,
        'tempos_manutencao': tempos_manutencao,
        'documentos_financeiro': documentos_financeiro,
        'documentos_contrato': documentos_contrato,
    }

    return render(request, 'contact/empresas_details.html', context)


@login_required
def adicionar_empresa_view(request):
    user = request.user
    if user.tipo_usuario not in ['admin', 'operador']:
        return redirect('contact:empresas_view')

    if request.method == 'POST':
        form = AdicionarEmpresaForm(request.POST, request=request)
        if form.is_valid():
            empresa = form.save(commit=False)
            empresa.criado_por = request.user
            empresa.save()
            return redirect('contact:empresas_view')
    else:
        form = AdicionarEmpresaForm()
    return render(request, 'contact/adicionar_empresa.html', {'form': form})

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

def add_documento(request, empresa_id):
    empresa = get_object_or_404(Empresa, id=empresa_id)
    
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            documento = form.save(commit=False)
            documento.empresa = empresa
            documento.save()
            return redirect('contact:empresas_details', empresa_id=empresa.id)
    else:
        form = DocumentoForm()
    
    return render(request, 'contact/add_documento.html', {'form': form, 'empresa': empresa})

def delete_documento(request, documento_id, empresa_id):
    documento = get_object_or_404(DocumentoEmpresa, id=documento_id)
    empresa_id = documento.empresa.id
    documento.delete()
    return redirect('contact:empresas_details', empresa_id=empresa_id)