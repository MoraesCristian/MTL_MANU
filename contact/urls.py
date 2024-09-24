from django.urls import path
from contact import views

app_name = 'contact'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('empresas/', views.empresas_view, name='empresas_view'),
    path('empresas/adicionar/', views.adicionar_empresa_view, name='adicionar_empresa'),
    path('empresas/<int:empresa_id>/', views.empresa_detalhes_view, name='empresas_details'),
    path('empresas/editar/<int:empresa_id>/', views.editar_empresa_view, name='edit_empresas'),
    path('create-user/', views.create_user_view, name='create_user'),
    path('list-users/<int:user_id>/edit/', views.edit_user_view, name='edit_user'),
    path('list-users/<int:user_id>/', views.user_detail_view, name='user_detail'),
    path('list-users/', views.list_users_view, name='list_user'),
    path('chamados/', views.listar_chamados, name='listar_chamados'),
    path('abrir_chamado/', views.abrir_chamado, name='abrir_chamado'),
    path('listar-chamados/', views.listar_chamados, name='listar_chamados'),
    path('chamado/<int:chamado_id>/', views.visualizar_chamado, name='visualizar_chamado'),
    path('chamado/<int:chamado_id>/chat/', views.load_chat, name='load_chat'),
    path('chamado/<int:chamado_id>/informacao_chamado/', views.load_informacao_chamado, name='load_informacao_chamado'),
    path('chamado/<int:chamado_id>/tarefas_a_realizar/', views.load_tarefas_a_realizar, name='load_tarefas_a_realizar'),
    path('tarefas/', views.buscar_tarefas, name='buscar_tarefas'),
    path('tarefas/criar/', views.criar_tarefa, name='criar_tarefa'),
    path('listar_tarefas/', views.listar_tarefas, name='listar_tarefas'),
    path('tarefas/<int:tarefa_id>/detalhes/', views.listar_detalhes_tarefa, name='listar_detalhes_tarefa'),
    path('tarefas/<int:tarefa_id>/detalhes/criar/', views.criar_detalhe_tarefa, name='criar_detalhe_tarefa'),
    path('areas/', views.listar_areas, name='listar_areas'),
    path('areas/criar/', views.criar_area, name='criar_area'),
    path('areas/<int:area_id>/', views.detalhes_area, name='detalhes_area'),
    path('profile/', views.profile_view, name='profile'),
]
