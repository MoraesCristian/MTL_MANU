from django.urls import path
from contact import views

app_name = 'contact'

urlpatterns = [
    path('', views.home_view, name='home'),  # Página principal
    path('empresas/', views.empresas_view, name='empresas'),
    path('chamados/', views.chamados_view, name='chamados'),
    path('profile/', views.profile_view, name='profile'),  # Página de perfil
]