from django.contrib import admin
from contact import models

@admin.register(models.Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'empresa', 'email', 'tipo_usuario')
    search_fields = ('first_name', 'last_name', 'email', 'tipo_usuario')
    list_per_page = 50
    list_max_show_all = 100
    list_display_links = ('first_name', 'last_name', 'email')


@admin.register(models.TempoManutencao)
class TempoManutencaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'empresa', 'tipo_manutencao', 'tempo')
    search_fields = ('empresa__razao_social', 'tipo_manutencao')
    list_per_page = 50
    list_max_show_all = 100
    list_display_links = ('empresa', 'tipo_manutencao')


@admin.register(models.DocumentoEmpresa)
class DocumentoEmpresaAdmin(admin.ModelAdmin):
    list_display = ('id', 'empresa', 'tipo_documento', 'descricao')
    search_fields = ('empresa__razao_social', 'tipo_documento', 'descricao')
    list_per_page = 50
    list_max_show_all = 100
    list_display_links = ('empresa', 'tipo_documento')


@admin.register(models.Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'empresa')
    search_fields = ('nome', 'empresa__razao_social')
    list_per_page = 50
    list_max_show_all = 100
    list_display_links = ('nome',)


@admin.register(models.Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    list_display = ('id', 'area', 'descricao')
    search_fields = ('descricao', 'area__nome')
    list_per_page = 50
    list_max_show_all = 100
    list_display_links = ('descricao',)


@admin.register(models.DetalheTarefa)
class DetalheTarefaAdmin(admin.ModelAdmin):
    list_display = ('id', 'tarefa', 'descricao')
    search_fields = ('descricao', 'tarefa__descricao')
    list_per_page = 50
    list_max_show_all = 100
    list_display_links = ('descricao',)


@admin.register(models.Chamado)
class ChamadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero_ordem', 'titulo', 'empresa', 'tipo_manutencao', 'status_chamado', 'data_criacao')
    search_fields = ('numero_ordem', 'titulo', 'empresa__razao_social', 'tipo_manutencao')
    list_per_page = 50
    list_max_show_all = 100
    list_display_links = ('numero_ordem', 'titulo')
    list_filter = ('tipo_manutencao', 'status_chamado', 'empresa')


@admin.register(models.DetalheTarefaPreenchido)
class DetalheTarefaPreenchidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'detalhe_tarefa', 'chamado', 'usuario', 'concluido', 'nao_comporta')
    search_fields = ('detalhe_tarefa__descricao', 'chamado__numero_ordem', 'usuario__email')
    list_per_page = 50
    list_max_show_all = 100
    list_display_links = ('detalhe_tarefa', 'chamado')


@admin.register(models.ImagemChamado)
class ImagemChamadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'chamado', 'data_upload')
    search_fields = ('chamado__numero_ordem',)
    list_per_page = 50
    list_max_show_all = 100
    list_display_links = ('chamado',)


@admin.register(models.Imagem)
class ImagemAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero_ordem', 'tarefa', 'detalhe_tarefa', 'tipo_imagem')
    search_fields = ('numero_ordem__numero_ordem', 'tarefa__descricao', 'detalhe_tarefa__descricao')
    list_per_page = 50
    list_max_show_all = 100
    list_display_links = ('numero_ordem', 'tarefa')


@admin.register(models.Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'chamado')
    search_fields = ('chamado__numero_ordem',)
    list_per_page = 50
    list_max_show_all = 100
    list_display_links = ('chamado',)


@admin.register(models.MensagemChat)
class MensagemChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat', 'usuario', 'data_envio', 'empresa')
    search_fields = ('chat__chamado__numero_ordem', 'usuario__email', 'empresa__razao_social')
    list_per_page = 50
    list_max_show_all = 100
    list_display_links = ('chat', 'usuario')


class EmpresaAreaTarefaAdmin(admin.ModelAdmin):
    list_display = ('empresa_nome', 'empresa_id', 'areas_da_empresa', 'tarefas_da_empresa')
    search_fields = ('empresa__razao_social', 'empresa__nome_fantasia')

    def empresa_nome(self, obj):
        return obj.razao_social
    empresa_nome.short_description = 'Empresa (Nome)'

    def empresa_id(self, obj):
        return obj.id
    empresa_id.short_description = 'Empresa (ID)'

    def areas_da_empresa(self, obj):
        areas = models.Area.objects.filter(empresa=obj)
        return ", ".join([area.nome for area in areas])
    areas_da_empresa.short_description = 'Áreas da Empresa'

    def tarefas_da_empresa(self, obj):
        areas = models.Area.objects.filter(empresa=obj)
        tarefas = models.Tarefa.objects.filter(area__in=areas)
        return ", ".join([tarefa.descricao for tarefa in tarefas])
    tarefas_da_empresa.short_description = 'Tarefas da Empresa'

# Registre a visualização personalizada
admin.site.register(models.Empresa, EmpresaAreaTarefaAdmin)