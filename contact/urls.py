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
    path('profile/', views.profile_view, name='profile'),
]
