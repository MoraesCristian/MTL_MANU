from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from contact.models import Chamado, Empresa, Tarefa, Area, DetalheTarefa,DetalheTarefaPreenchido, ImagemChamado
from django.http import HttpResponseForbidden, JsonResponse
from contact.forms.chamado_forms import ChamadoForm , DetalheTarefaForm, AdicionarPrestadoraServicoForm, ImagemChamadoForm
from contact.forms.area_forms import AreaForm
from contact.forms.tarefa_forms import TarefaForm
from collections import defaultdict

from django.contrib import messages
from django.db.models import Q
from django.utils.dateparse import parse_date
 
@login_required
def listar_chamados(request):
    user = request.user
    chamados = Chamado.objects.none()
    empresas = None
    empresa_filter = request.GET.get('empresa_id')
    data_abertura_inicio = request.GET.get('data_abertura_inicio')
    data_abertura_fim = request.GET.get('data_abertura_fim')
    status_chamado_filter = request.GET.get('status_chamado')
    search = request.GET.get('search')
    prioridade_filter = request.GET.get('prioridade_chamado')

    if user.tipo_usuario in ['admin', 'operador']:
        empresas = Empresa.objects.all()
        chamados = Chamado.objects.all()

    elif user.tipo_usuario == 'manager':
        empresa_usuario = user.empresa
        empresas = Empresa.objects.filter(filial_de=empresa_usuario) | Empresa.objects.filter(id=empresa_usuario.id)
        chamados = Chamado.objects.filter(empresa__in=empresas)

    elif user.tipo_usuario == 'user':
        empresa_usuario = user.empresa
        chamados = Chamado.objects.filter(prestadora_servico=empresa_usuario)
        empresas = Empresa.objects.filter(id=empresa_usuario.id)

    else:
        empresa_usuario = user.empresa
        empresas = Empresa.objects.filter(filial_de=empresa_usuario) | Empresa.objects.filter(id=empresa_usuario.id)
        chamados = Chamado.objects.filter(empresa__in=empresas)

    if empresa_filter:
        chamados = chamados.filter(empresa_id=empresa_filter)

    if data_abertura_inicio:
        data_inicio = parse_date(data_abertura_inicio)
        if data_inicio:
            chamados = chamados.filter(data_criacao__gte=data_inicio)

    if data_abertura_fim:
        data_fim = parse_date(data_abertura_fim)
        if data_fim:
            chamados = chamados.filter(data_criacao__lte=data_fim)

    if status_chamado_filter:
        chamados = chamados.filter(status_chamado=status_chamado_filter)

    if search:
        chamados = chamados.filter(
            Q(empresa__cnpj__icontains=search) |
            Q(numero_ordem__icontains=search) |
            Q(empresa_nome_fantasia__icontains=search)
        )

    if prioridade_filter:
        chamados = chamados.filter(prioridade_chamado=prioridade_filter)
        
    chamados = chamados.order_by(
        'prioridade_chamado',
        'data_criacao'
    )

    context = {
        'chamados': chamados,
        'empresas': empresas,
        'empresa_id': empresa_filter,
        'user_tipo': user.tipo_usuario,
    }
    return render(request, 'contact/listar_chamados.html', context)


@login_required
def abrir_chamado(request):
    user = request.user

    if user.tipo_usuario == 'manager':
        if user.empresa is None:
            return HttpResponseForbidden("Usuário não está vinculado a nenhuma empresa.")
        empresas = Empresa.objects.filter(Q(id=user.empresa.id) | Q(filial_de=user.empresa))
    else:
        empresas = Empresa.objects.all()
        
    if request.method == 'POST':
        form = ChamadoForm(request.POST, request.FILES, user=user, empresas=empresas)
        if form.is_valid():
            chamado = form.save(commit=False)
            chamado.criado_por = request.user
            chamado.empresa = form.cleaned_data['empresa_nome_fantasia']
            
            if chamado.area_chamado and chamado.tarefa:
                chamado.titulo = f'{chamado.tarefa}'

            chamado.save()

            imagens = request.FILES.getlist('imagens')
            for imagem in imagens:
                ImagemChamado.objects.create(chamado=chamado, imagem=imagem)
            
            if chamado.tarefa:
                detalhes = DetalheTarefa.objects.filter(tarefa=chamado.tarefa)
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

@login_required
def load_empresa_address(request):
    empresa_id = request.GET.get('empresa_id')
    empresa = Empresa.objects.get(id=empresa_id)
    address = f"{empresa.logradouro}, {empresa.estado}"
    return JsonResponse({'address': address})


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


def criar_area(request):
    if not (request.user.tipo_usuario == 'admin' or request.user.tipo_usuario == 'gerente'):
        messages.error(request, "Você não tem permissão para criar áreas.")
        return redirect('contact:listar_areas') 
    
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
    if not (request.user.tipo_usuario == 'admin' or request.user.tipo_usuario == 'gerente'):
        messages.error(request, "Você não tem permissão para criar áreas.")
        return redirect('contact:listar_tarefas') 
    
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
    if not (request.user.tipo_usuario == 'admin' or request.user.tipo_usuario == 'gerente'):
        messages.error(request, "Você não tem permissão para criar áreas.")
        return redirect('contact:listar_detalhes_tarefa', tarefa_id=tarefa_id) 
    
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
            chamado.prestadora_servico = form.cleaned_data['prestadora_servico']
            chamado.save()
            return redirect('contact:visualizar_chamado', chamado_id=chamado.id)
    else:
        form = AdicionarPrestadoraServicoForm(instance=chamado)

    prestadora_atual = chamado.prestadora_servico

    return render(request, 'contact/adicionar_prestadora_servico.html', {
        'form': form,
        'chamado': chamado,
        'prestadora_atual': prestadora_atual
    })

