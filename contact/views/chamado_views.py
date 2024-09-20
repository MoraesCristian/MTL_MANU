from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from contact.models import Chamado, Empresa, Tarefa, Area
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from contact.forms.chamado_forms import ChamadoForm
from contact.forms.area_forms import AreaForm
from contact.forms.tarefa_forms import TarefaForm


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

    if user.tipo_usuario == 'cliente':
        if user.empresa is None:
            return HttpResponseForbidden("Usuário não está vinculado a nenhuma empresa.")

        empresa_id = user.empresa.id
        empresas = Empresa.objects.filter(id=empresa_id)
    else:
        empresas = Empresa.objects.all()
        
    if request.method == 'POST':
        form = ChamadoForm(request.POST, empresas=empresas)
        if form.is_valid():
            chamado = form.save(commit=False) 
            chamado.criado_por = request.user
            chamado.empresa = form.cleaned_data['empresa_nome_fantasia']
            chamado.save()
            return redirect('contact:listar_chamados')

    else:
        if request.user.is_superuser:
            form = ChamadoForm(empresas=empresas)
        else:
            form = ChamadoForm(user=request.user, empresas=empresas)
    
    return render(request, 'contact/abrir_chamado.html', {'form': form, 'empresas': empresas})

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
    areas = Area.objects.all()
    return render(request, 'contact/listar_areas.html', {'areas': areas})

@login_required
def detalhes_area(request, area_id):
    area = Area.objects.get(id=area_id)
    descricoes = Tarefa.objects.filter(area=area)
    return render(request, 'contact/detalhes_area.html', {'area': area, 'descricoes': descricoes})

@login_required
def listar_tarefas(request):
    tarefas = Tarefa.objects.all()
    return render(request, 'contact/listar_tarefas.html', {'tarefas': tarefas})

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

