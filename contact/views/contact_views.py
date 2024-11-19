import pandas as pd   
from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.db.models.functions import TruncMonth
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from contact.models import Chamado, Empresa


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not email or not password:
            messages.error(request, "Por favor, insira o email e a senha")
            return redirect('contact:login')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Email ou senha inválidos")
            return redirect('login')
    
    return render(request, 'contact/login.html')

@login_required
def home_view(request):
    user = request.user
    empresa_selecionada_id = request.GET.get('empresa_id')
    date_filter = request.GET.get('date_filter')
    cnpj_padrao = '00.000.000/0000-00'

    chamados = None
    chamados_por_mes_abertos = None
    chamados_por_mes_concluidos = None
    title = 'Chamados por Status'
    status_totals = {}

    status_colors = {
        'aberto': '#1500ff',
        'concluido': '#09c600',
        'executando': '#e9ff00',
        'rejeitado': '#ff0000',
        'assinatura': '#e0bb00',
        'Nenhum dado': '#898989'
    }

    date_limit = None
    if date_filter == '7':
        date_limit = timezone.now() - timedelta(days=7)
    elif date_filter == '30':
        date_limit = timezone.now() - timedelta(days=30)
    elif date_filter == '60':
        date_limit = timezone.now() - timedelta(days=60)
    elif date_filter == '90':
        date_limit = timezone.now() - timedelta(days=90)

    if user.tipo_usuario in ['admin', 'operador']:
        if empresa_selecionada_id:
            empresas_ids = list(Empresa.objects.filter(Q(id=empresa_selecionada_id) | Q(filial_de_id=empresa_selecionada_id)).values_list('id', flat=True))
            chamados = Chamado.objects.filter(empresa_id__in=empresas_ids)
            empresa_nome_fantasia = Empresa.objects.filter(id=empresa_selecionada_id).values_list('nome_fantasia', flat=True).first()
            title = f'Chamados por Status - {empresa_nome_fantasia}'
        else:
            chamados = Chamado.objects.all()
            title = 'Chamados por Status - Todas as Empresas'

    elif user.tipo_usuario == 'manager':
        user_empresa = user.empresa
        empresas_visiveis = list(Empresa.objects.filter(Q(id=user_empresa.id) | Q(filial_de=user_empresa)).values_list('id', flat=True))
        if empresa_selecionada_id:
            if int(empresa_selecionada_id) in empresas_visiveis:
                empresas_ids = list(Empresa.objects.filter(Q(id=empresa_selecionada_id) | Q(filial_de_id=empresa_selecionada_id)).values_list('id', flat=True))
                chamados = Chamado.objects.filter(empresa_id__in=empresas_ids)
                empresa_nome_fantasia = Empresa.objects.filter(id=empresa_selecionada_id).values_list('nome_fantasia', flat=True).first()
                title = f'Chamados por Status - {empresa_nome_fantasia}'
            else:
                chamados = Chamado.objects.none()  # Nenhuma empresa selecionada visível
        else:
            chamados = Chamado.objects.filter(empresa_id__in=empresas_visiveis)
            title = f'Chamados por Status - {user_empresa.nome_fantasia} e Filiais'

    elif user.tipo_usuario == 'user':
        chamados = Chamado.objects.filter(prestadora_servico=user.empresa)
        title = f'Chamados por Status - {user.empresa.nome_fantasia}'

    if date_limit:
        chamados = chamados.filter(data_criacao__gte=date_limit)

    # Contagem de chamados abertos por mês
    chamados_por_mes_abertos = chamados.annotate(mes=TruncMonth('data_criacao')).values('mes').annotate(
        abertos=Count('id')
    ).order_by('mes')

    # Contagem de chamados concluídos por mês
    chamados_por_mes_concluidos = chamados.filter(status_chamado='concluido').annotate(mes=TruncMonth('data_fim_chamado')).values('mes').annotate(
        concluidos=Count('id')
    ).order_by('mes')

    status_totals = chamados.values('status_chamado').annotate(total=Count('id')).order_by()

    df = pd.DataFrame(list(status_totals))

    if df.empty:
        df = pd.DataFrame({'status_chamado': ['Nenhum dado'], 'total': [0]})
    else:
        status_totals = df.set_index('status_chamado')['total'].to_dict()

    graph_data = {
        'labels': df['status_chamado'].tolist(),
        'datasets': [{
            'data': df['total'].tolist(),
            'backgroundColor': [status_colors[status] for status in df['status_chamado']]
        }]
    }

    # Tradução manual dos meses
    meses_traduzidos = {
        1: 'Janeiro',
        2: 'Fevereiro',
        3: 'Março',
        4: 'Abril',
        5: 'Maio',
        6: 'Junho',
        7: 'Julho',
        8: 'Agosto',
        9: 'Setembro',
        10: 'Outubro',
        11: 'Novembro',
        12: 'Dezembro'
    }

    meses_abertos = [meses_traduzidos[chamado['mes'].month] for chamado in chamados_por_mes_abertos]
    chamados_abertos = [chamado['abertos'] for chamado in chamados_por_mes_abertos]

    meses_concluidos = [meses_traduzidos[chamado['mes'].month] for chamado in chamados_por_mes_concluidos]
    chamados_concluidos = [chamado['concluidos'] for chamado in chamados_por_mes_concluidos]

    # Garantir que os meses estejam alinhados
    todos_os_meses = sorted(set(meses_abertos + meses_concluidos), key=lambda x: list(meses_traduzidos.values()).index(x))

    chamados_abertos_por_mes = {mes: 0 for mes in todos_os_meses}
    chamados_concluidos_por_mes = {mes: 0 for mes in todos_os_meses}

    for chamado in chamados_por_mes_abertos:
        mes = meses_traduzidos[chamado['mes'].month]
        chamados_abertos_por_mes[mes] = chamado['abertos']

    for chamado in chamados_por_mes_concluidos:
        mes = meses_traduzidos[chamado['mes'].month]
        chamados_concluidos_por_mes[mes] = chamado['concluidos']

    bar_chart_data = {
        'labels': todos_os_meses,
        'datasets': [
            {
                'label': 'Chamados Abertos',
                'data': [chamados_abertos_por_mes[mes] for mes in todos_os_meses],
                'backgroundColor': '#1500ff'
            },
            {
                'label': 'Chamados Concluídos',
                'data': [chamados_concluidos_por_mes[mes] for mes in todos_os_meses],
                'backgroundColor': '#09c600'
            }
        ]
    }

    if user.tipo_usuario == 'manager':
        empresas = Empresa.objects.filter(Q(id=user_empresa.id) | Q(filial_de=user_empresa)).values('id', 'nome_fantasia')
        
    elif user.tipo_usuario == 'user':
        empresas_ids = Chamado.objects.filter(prestadora_servico=user.empresa).values_list('empresa_id', flat=True).distinct()
        empresas = Empresa.objects.filter(id__in=empresas_ids).values('id', 'nome_fantasia')
    
    else:
        empresas = Empresa.objects.values('id', 'nome_fantasia').order_by('nome_fantasia')

    return render(request, 'contact/home.html', {
        'title': title,
        'chamados': chamados,
        'total_chamados': chamados.count(),
        'status_totals': status_totals,
        'graph_data': graph_data,
        'bar_chart_data': bar_chart_data,
        'empresas': empresas,
        'empresa_selecionada_id': empresa_selecionada_id,
        'date_filter': date_filter
    })


    
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'contact/password_reset.html'