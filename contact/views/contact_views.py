import plotly.express as px
import pandas as pd   
from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from contact.models import Chamado, Empresa
from django.db.models.functions import TruncMonth


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

from django.db.models.functions import TruncMonth

@login_required
def home_view(request):
    user = request.user
    empresa_selecionada_id = request.GET.get('empresa_id')  # Captura a empresa selecionada (None se não selecionada)
    date_filter = request.GET.get('date_filter')  # Captura o filtro de datas (None se não selecionado)
    cnpj_padrao = '00.000.000/0000-00'

    chamados = None
    title = 'Chamados por Status'  # Título padrão
    status_totals = {}

    # Dicionário de cores para os status
    status_colors = {
        'aberto': '#1500ff',
        'concluido': '#09c600',
        'executando': '#e9ff00',
        'rejeitado': '#ff0000',
        'assinatura': '#e0bb00',
        'Nenhum dado': '#898989'
    }

    # Determina a data inicial com base no filtro
    date_limit = None
    if date_filter == '7':
        date_limit = timezone.now() - timedelta(days=7)
    elif date_filter == '30':
        date_limit = timezone.now() - timedelta(days=30)
    elif date_filter == '60':
        date_limit = timezone.now() - timedelta(days=60)
    elif date_filter == '90':
        date_limit = timezone.now() - timedelta(days=90)

    # Verificar o tipo de usuário
    if user.tipo_usuario in ['admin', 'operador']:
        chamados = Chamado.objects.values('status_chamado').annotate(total=Count('id'))
        if date_limit:
            chamados = chamados.filter(data_criacao__gte=date_limit)
        if not empresa_selecionada_id:
            empresa_padrao = Empresa.objects.filter(cnpj=cnpj_padrao).first()
            empresa_selecionada_id = empresa_padrao.id if empresa_padrao else None
        if empresa_selecionada_id:
            chamados = Chamado.objects.filter(empresa_id=empresa_selecionada_id).values('status_chamado').annotate(total=Count('id'))
            if date_limit:
                chamados = chamados.filter(data_criacao__gte=date_limit)
            empresa_nome_fantasia = Empresa.objects.filter(id=empresa_selecionada_id).values_list('nome_fantasia', flat=True).first()
            title = f'Chamados por Status - {empresa_nome_fantasia}'
    elif user.tipo_usuario == 'user':
        chamados = Chamado.objects.filter(prestadora_servico=user.empresa).values('status_chamado').annotate(total=Count('id'))
        if date_limit:
            chamados = chamados.filter(data_criacao__gte=date_limit)
        if empresa_selecionada_id:
            chamados = chamados.filter(empresa_id=empresa_selecionada_id).values('status_chamado').annotate(total=Count('id'))
            if date_limit:
                chamados = chamados.filter(data_criacao__gte=date_limit)
            empresa_nome_fantasia = Empresa.objects.filter(id=empresa_selecionada_id).values_list('nome_fantasia', flat=True).first()
            title = f'Chamados por Status - {empresa_nome_fantasia}'
    elif user.tipo_usuario == 'manager':
        user_empresa = user.empresa
        if Empresa.objects.filter(filial_de=user_empresa).exists():
            empresas_visiveis = list(Empresa.objects.filter(filial_de=user_empresa).values_list('id', flat=True))
            empresas_visiveis.append(user_empresa.id)
        else:
            empresas_visiveis = [user_empresa.id]
        chamados = Chamado.objects.filter(empresa_id__in=empresas_visiveis).values('status_chamado').annotate(total=Count('id'))
        if date_limit:
            chamados = chamados.filter(data_criacao__gte=date_limit)
        title = f'Chamados por Status - {user_empresa.nome_fantasia}'
        if empresa_selecionada_id and int(empresa_selecionada_id) in empresas_visiveis:
            chamados = chamados.filter(empresa_id=empresa_selecionada_id).values('status_chamado').annotate(total=Count('id'))
            if date_limit:
                chamados = chamados.filter(data_criacao__gte=date_limit)
            empresa_nome_fantasia = Empresa.objects.filter(id=empresa_selecionada_id).values_list('nome_fantasia', flat=True).first()
            title = f'Chamados por Status - {empresa_nome_fantasia}'
        empresas_visiveis_queryset = Empresa.objects.filter(id__in=empresas_visiveis).values('id', 'nome_fantasia')

    df = pd.DataFrame(list(chamados))
    if df.empty:
        df = pd.DataFrame({'status_chamado': ['Nenhum dado'], 'total': [0]})
    else:
        status_totals = df.set_index('status_chamado')['total'].to_dict()

    # Converte os dados do gráfico para JSON para passar para o template
    graph_data = {
        'labels': df['status_chamado'].tolist(),
        'datasets': [{
            'data': df['total'].tolist(),
            'backgroundColor': [status_colors[status] for status in df['status_chamado']]
        }]
    }

    # Dados do gráfico de barras
    chamados_por_mes = Chamado.objects.annotate(mes=TruncMonth('data_criacao')).values('mes').annotate(
        abertos=Count('id', filter=Q(status_chamado='aberto')),
        concluidos=Count('id', filter=Q(status_chamado='concluido'))
    ).order_by('mes')

    meses = [chamado['mes'].strftime('%B') for chamado in chamados_por_mes]
    chamados_abertos = [chamado['abertos'] for chamado in chamados_por_mes]
    chamados_concluidos = [chamado['concluidos'] for chamado in chamados_por_mes]

    bar_chart_data = {
        'labels': meses,
        'datasets': [
            {
                'label': 'Chamados Abertos',
                'data': chamados_abertos,
                'backgroundColor': '#1500ff'
            },
            {
                'label': 'Chamados Concluídos',
                'data': chamados_concluidos,
                'backgroundColor': '#09c600'
            }
        ]
    }
    
    if user.tipo_usuario == 'manager':
        empresas = empresas_visiveis_queryset
    else:
        empresas = Empresa.objects.values('id', 'nome_fantasia').distinct()
        
        
    return render(request, 'contact/home.html', {
        'graph_data': graph_data, #PIE
        'bar_chart_data': bar_chart_data, #BAR
        'empresas': empresas,
        'empresa_id': empresa_selecionada_id,
        'status_totals': status_totals,
        'status_colors': status_colors,
        'title': title,
        'date_filter': date_filter
    })

    
    
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'contact/password_reset.html'