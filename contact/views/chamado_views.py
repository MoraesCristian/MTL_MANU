from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from contact.models import Chamado, Empresa, Tarefa
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from contact.forms.chamado_forms import ChamadoForm


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

    # Verifique se o usuário tem a empresa vinculada
    if user.tipo_usuario == 'cliente':
        if user.empresa is None:
            return HttpResponseForbidden("Usuário não está vinculado a nenhuma empresa.")
        
        # Obtenha a empresa associada ao usuário
        empresa_id = user.empresa.id
        empresas = Empresa.objects.filter(id=empresa_id)
    else:
        empresas = Empresa.objects.all()
    
    # Debug: Verifique se as empresas estão sendo carregadas corretamente
    print(f'Empresas carregadas: {empresas}')

    if request.method == 'POST':
        form = ChamadoForm(request.POST, empresas=empresas)
        if form.is_valid():
            chamado = form.save(commit=False)
            chamado.usuario = user
            chamado.save()
            return redirect('contact:listar_chamados')
    else:
        form = ChamadoForm(empresas=empresas)

    return render(request, 'contact/abrir_chamado.html', {
        'form': form,
        'empresas': empresas,
    })

def get_tarefas(request):
    area = request.GET.get('area')
    if area:
        tarefas = Tarefa.objects.filter(area=area).values('id', 'descricao')
        tarefas_list = list(tarefas)
        return JsonResponse(tarefas_list, safe=False)
    return JsonResponse({'error': 'Área não especificada'}, status=400)

