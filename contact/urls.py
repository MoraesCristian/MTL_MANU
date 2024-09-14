from django.urls import path
from contact import views

app_name = 'contact'

urlpatterns = [
    path('', views.home_view, name='home'),  # Página principal
    path('empresas/', views.empresas_view, name='empresas_view'),
    path('empresas/adicionar/', views.adicionar_empresa_view, name='adicionar_empresa'),
    path('empresas/<int:empresa_id>/', views.empresa_detalhes_view, name='empresas_details'),
    path('empresas/editar/<int:empresa_id>/', views.editar_empresa_view, name='edit_empresas'),
    path('chamados/', views.chamados_view, name='chamados'),
    path('profile/', views.profile_view, name='profile'),  # Página de perfil
]