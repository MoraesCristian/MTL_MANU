from django.contrib import admin
from contact import models

@admin.register(models.Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('id','razao_social','cnpj','email_empresa','telefone')
    #list_filter = ('razao_social',)
    search_fields = ('razao_social','cnpj','razao_social','nome_fantasia',)
    list_per_page = 20
    list_max_show_all = 100
    list_display_links = ('razao_social','cnpj','email_empresa','telefone')

@admin.register(models.Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','empresa','email')
    search_fields = ('first_name','last_name','email',)
    list_per_page = 50
    list_max_show_all = 100
    list_display_links = ('first_name','last_name','email')
    
@admin.register(models.Chamado)
class ChamadoAdmin(admin.ModelAdmin):
    ...

@admin.register(models.ImagemChamado)
class ImagemChamadoAdmin(admin.ModelAdmin):
    ...