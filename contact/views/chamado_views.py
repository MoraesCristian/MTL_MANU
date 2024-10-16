from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from contact.models import Chamado, Empresa, Tarefa, Area, DetalheTarefa,DetalheTarefaPreenchido
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from contact.forms.chamado_forms import ChamadoForm , DetalheTarefaForm, AdicionarPrestadoraServicoForm
from contact.forms.area_forms import AreaForm
from contact.forms.tarefa_forms import TarefaForm
from collections import defaultdict


@login_required
def listar_chamados(request):
    user = request.user
    chamados = Chamado.objects.none() 
    empresas = None

    if user.tipo_usuario == 'admin' or user.tipo_usuario =='operador' :
        empresa_filter = request.GET.get('empresa')
        chamados = Chamado.objects.all()
        if empresa_filter:
            chamados = chamados.filter(empresa__nome_fantasia=empresa_filter)
        empresas = Empresa.objects.all()

    elif user.tipo_usuario == 'manager':
        empresa_filter = request.GET.get('empresa')
        empresa_usuario = user.empresa
        chamados = Chamado.objects.filter(empresa=empresa_usuario)
        if empresa_filter:
            chamados = chamados.filter(empresa__nome_fantasia=empresa_filter)
        empresas = Empresa.objects.filter(id=empresa_usuario.id)

    elif user.tipo_usuario == 'user':
        empresa_usuario = user.empresa
        chamados = Chamado.objects.filter(prestadora_servico=empresa_usuario)
        empresas = Empresa.objects.filter(id=empresa_usuario.id)

    else:
        # Para outros tipos de usuários, como clientes, mostrando chamados vinculados à empresa deles.
        empresa_usuario = user.empresa
        chamados = Chamado.objects.filter(empresa=empresa_usuario)
        empresas = Empresa.objects.filter(id=empresa_usuario.id)

    context = {
        'chamados': chamados,
        'empresas': empresas,
        'user_tipo': user.tipo_usuario,
    }
    return render(request, 'contact/listar_chamados.html', context)

@login_required
def abrir_chamado(request):
    user = request.user

    if user.tipo_usuario == 'manager':
        if user.empresa is None:
            return HttpResponseForbidden("Usuário não está vinculado a nenhuma empresa.")
        empresas = Empresa.objects.filter(id=user.empresa.id)
    else:
        empresas = Empresa.objects.all()
        
    if request.method == 'POST':
        form = ChamadoForm(request.POST, user=user, empresas=empresas)
        if form.is_valid():
            chamado = form.save(commit=False)
            chamado.criado_por = request.user
            chamado.empresa = form.cleaned_data['empresa_nome_fantasia']
            chamado.save()
            if chamado.tarefa:
                detalhes = DetalheTarefa.objects.filter(tarefa=chamado.tarefa)
                for detalhe in detalhes:
                    print(f"- {detalhe.descricao}")
                
                for detalhe in detalhes:
                    DetalheTarefaPreenchido.objects.create(
                        detalhe_tarefa=detalhe,
                        chamado=chamado,
                        usuario=request.user,
                    )

            return redirect('contact:listar_chamados')
    else:
        form = ChamadoForm(user=user, empresas=empresas)
    
    return render(request, 'contact/abrir_chamado.html', {'form': form})


def buscar_tarefas(request):
    area_id = request.GET.get('area')
    tarefas = Tarefa.objects.filter(area_id=area_id).values('id', 'descricao')
    return JsonResponse(list(tarefas), safe=False)

@login_required
def criar_area(request):
    if request.method == 'POST':
        form = AreaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact:listar_areas')
    else:
        form = AreaForm()
    
    return render(request, 'contact/criar_area.html', {'form': form})

@login_required
def listar_areas(request):
    areas = Area.objects.select_related('empresa').all()
    return render(request, 'contact/listar_areas.html', {'areas': areas})


@login_required
def detalhes_area(request, area_id):
    area = Area.objects.get(id=area_id)
    descricoes = Tarefa.objects.filter(area=area)
    return render(request, 'contact/detalhes_area.html', {'area': area, 'descricoes': descricoes})

@login_required
def listar_tarefas(request):
    tarefas = Tarefa.objects.select_related('area', 'area__empresa').all()
    tarefas_por_area = defaultdict(list)

    for tarefa in tarefas:
        tarefas_por_area[tarefa.area].append(tarefa)

    return render(request, 'contact/listar_tarefas.html', {'tarefas_por_area': dict(tarefas_por_area)})


@login_required
def criar_tarefa(request):
    if request.method == 'POST':
        form = TarefaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact:listar_tarefas')
    else:
        form = TarefaForm()
    
    return render(request, 'contact/criar_tarefa.html', {'form': form})

@login_required
def ajax_load_areas(request):
    empresa_id = request.GET.get('empresa_id')
    areas = Area.objects.filter(empresa_id=empresa_id).order_by('nome')
    return JsonResponse(list(areas.values('id', 'nome')), safe=False)

@login_required
def ajax_load_tarefas(request):
    area_id = request.GET.get('area_id')
    tarefas = Tarefa.objects.filter(area_id=area_id).order_by('descricao')
    return JsonResponse(list(tarefas.values('id', 'descricao')), safe=False)

@login_required
def listar_detalhes_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    detalhes = DetalheTarefa.objects.filter(tarefa=tarefa)
    return render(request, 'contact/listar_detalhes_tarefa.html', {'tarefa': tarefa, 'detalhes': detalhes})

@login_required
def criar_detalhe_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    
    if request.method == 'POST':
        form = DetalheTarefaForm(request.POST, tarefa=tarefa)
        if form.is_valid():
            detalhe_tarefa = form.save(commit=False)
            detalhe_tarefa.tarefa = tarefa
            detalhe_tarefa.save()
            return redirect('contact:listar_detalhes_tarefa', tarefa_id=tarefa_id)
    else:
        form = DetalheTarefaForm(tarefa=tarefa)
    
    return render(request, 'contact/criar_detalhe_tarefa.html', {'form': form, 'tarefa': tarefa})

@login_required
def adicionar_prestadora_servico_view(request, chamado_id):
    chamado = get_object_or_404(Chamado, id=chamado_id)
    
    if request.method == 'POST':
        form = AdicionarPrestadoraServicoForm(request.POST, instance=chamado)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('contact:visualizar_chamado', chamado_id=chamado.id)
        else:
            # Capture os erros de validação
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = AdicionarPrestadoraServicoForm(instance=chamado)
    
    prestadora_atual = chamado.prestadora_servico
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'contact/adicionar_prestadora_servico.html', {
            'form': form,
            'chamado': chamado,
            'prestadora_atual': prestadora_atual
        })
    
    return render(request, 'contact/adicionar_prestadora_servico.html', {
        'form': form,
        'chamado': chamado,
        'prestadora_atual': prestadora_atual
    })

