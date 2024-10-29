from django.urls import path
from contact import views

app_name = 'contact'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('cadastros/', views.cadastros_view, name='cadastros'),
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
    path('chamado/<int:chamado_id>/tarefa/<int:tarefa_id>/detalhe/<int:detalhe_tarefa_id>/', views.detalhe_tarefa_view, name='detalhe_tarefa'),
    path('chamado/<int:chamado_id>/tarefa/<int:tarefa_id>/detalhe/<int:detalhe_tarefa_id>/editar/', views.detalhe_tarefa_edit_view, name='detalhe_tarefa_edit'),
    path('chamado/<int:chamado_id>/atualizar-status/', views.atualizar_status_chamado_view, name='atualizar_status_chamado'),
    path('chamado/<int:chamado_id>/adicionar_prestadora_servico/', views.adicionar_prestadora_servico_view, name='adicionar_prestadora_servico'),
    path('excluir_imagem/<int:imagem_id>/', views.excluir_imagem, name='excluir_imagem'),
    path('tarefas/', views.buscar_tarefas, name='buscar_tarefas'),
    path('tarefas/criar/', views.criar_tarefa, name='criar_tarefa'),
    path('ajax/load-areas/', views.ajax_load_areas, name='ajax_load_areas'),
    path('ajax/load-tarefas/', views.ajax_load_tarefas, name='ajax_load_tarefas'),
    path('listar_tarefas/', views.listar_tarefas, name='listar_tarefas'),
    path('tarefas/<int:tarefa_id>/detalhes/', views.listar_detalhes_tarefa, name='listar_detalhes_tarefa'),
    path('tarefas/<int:tarefa_id>/detalhes/criar/', views.criar_detalhe_tarefa, name='criar_detalhe_tarefa'),
    path('areas/', views.listar_areas, name='listar_areas'),
    path('areas/criar/', views.criar_area, name='criar_area'),
    path('areas/<int:area_id>/', views.detalhes_area, name='detalhes_area'),
    path('profile/', views.profile_view, name='profile'),
    path('configuracao/', views.configuracao, name='configuracao'),
]

