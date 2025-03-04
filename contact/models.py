import re
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.db.models import UniqueConstraint


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, first_name, last_name, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = [
        ('admin', 'Administrador'),
        ('operador', 'Operador'),
        ('manager', 'Cliente'),
        ('user', 'Terceiro'),
    ]
    id = models.AutoField(primary_key=True) 
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE, null=True, blank=True)
    cpf = models.CharField(max_length=50, blank=True)
    telefone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    tipo_usuario = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='user')
    criado_por = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='usuarios_criados')
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def can_create_user(self):
        return self.tipo_usuario in ['admin', 'operador']

    def can_create_admin(self):
        return self.tipo_usuario == 'admin'

    def can_create_manager(self):
        return self.tipo_usuario in ['admin', 'operador']

    @property
    def tipo_usuario_display(self):
        return dict(self.USER_TYPE_CHOICES).get(self.tipo_usuario, 'Desconhecido')
    
    
class Empresa(models.Model):
    id = models.AutoField(primary_key=True)
    razao_social = models.CharField(max_length=255)
    nome_fantasia = models.CharField(max_length=255, blank=True)
    cnpj = models.CharField(max_length=18, unique=True)
    is_estadual = models.CharField(max_length=18, blank=True)
    is_municipal = models.CharField(max_length=18, blank=True)
    logradouro = models.CharField(max_length=255, blank=True)
    estado = models.CharField(max_length=2, choices=[
        ('AC','Acre'),
        ('AL','Alagoas'),
        ('AP','Amapá'),
        ('AM','Amazonas'),
        ('BA','Bahia'),
        ('CE','Ceará'),
        ('ES','Espírito Santo'),
        ('GO','Goiás'),
        ('MA','Maranhão'),
        ('MT','Mato Grosso'),
        ('MS','Mato Grosso do Sul'),
        ('MG','Minas Gerais'),
        ('PA','Pará'),
        ('PB','Paraíba'),
        ('PR','Paraná'),
        ('PE','Pernambuco'),
        ('PI','Piauí'),
        ('RJ','Rio de Janeiro'),
        ('RN','Rio Grande do Norte'),
        ('RS','Rio Grande do Sul'),
        ('RO','Rondônia'),
        ('RR','Roraima'),
        ('SC','Santa Catarina'),
        ('SP','São Paulo'),
        ('SE','Sergipe'),
        ('TO','Tocantins'),
    ],
    blank=False
    )
    telefone = models.CharField(max_length=50)
    email_empresa = models.EmailField(max_length=255)
    observacao = models.CharField(max_length=255)
    prefixo = models.CharField(max_length=15, blank=True, default='') 
    criado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='empresas_criadas')
    filial_de = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='filiais')
    responsavel_empre = models.CharField(max_length=255, blank=True)
    email_responsavel = models.EmailField(max_length=255, blank=True)
    
    def clean(self):
        self.razao_social = self.remove_special_characters(self.razao_social)
        self.nome_fantasia = self.remove_special_characters(self.nome_fantasia)
        if not self.razao_social or not self.nome_fantasia:
            raise ValidationError('Razão social e nome fantasia não podem estar vazios ou conter caracteres especiais.')
        
    @staticmethod
    def remove_special_characters(value):
        return re.sub(r'[^A-Za-z0-9 ]+', '', value)

    def __str__(self):
        return self.razao_social

class TempoManutencao(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='tempos_manutencao')
    tipo_manutencao = models.CharField(max_length=255, choices=[
        ('preventiva', 'Preventiva'),
        ('emergial', 'Emergial'),
        ('corretiva', 'Corretiva'),
    ])
    tempo = models.DurationField(help_text='Tempo em dias, horas, etc.')

    def __str__(self):
        return f'{self.empresa.nome_fantasia} - {self.tipo_manutencao}: {self.tempo}'

class DocumentoEmpresa(models.Model):
    TIPOS_DOCUMENTO = [
        ('financeiro', 'Financeiro'),
        ('contrato', 'Contrato'),
    ]

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='documentos')
    tipo_documento = models.CharField(max_length=50, choices=TIPOS_DOCUMENTO)
    descricao = models.CharField(max_length=255, blank=True, null=True)
    documento = models.FileField(upload_to='documentos_empresa/')

    def __str__(self):
        return f'{self.empresa.nome_fantasia} - {self.get_tipo_documento_display()}'

class Area(models.Model):
    nome = models.CharField(max_length=255)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['nome', 'empresa'], name='unique_area_per_empresa')
        ]

    def __str__(self):
        return self.nome
   
    
class Tarefa(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.area.nome} - {self.descricao}'
    
    
class DetalheTarefa(models.Model):
    tarefa = models.ForeignKey(Tarefa, on_delete=models.CASCADE, related_name='detalhes')
    descricao = models.CharField(max_length=255)
    
    def __str__(self):
        return f'{self.tarefa.descricao} - {self.descricao}'


class Chamado(models.Model):
    id = models.AutoField(primary_key=True)
    numero_ordem = models.CharField(max_length=20, unique=True, editable=False)
    titulo = models.CharField(max_length=255)
    descricao = models.TextField(blank=True)
    tipo_manutencao = models.CharField(max_length=255, choices=[
        ('preventiva', 'Preventiva'),
        ('emergencial', 'Emergencial'),
        ('corretiva', 'Corretiva'),
    ])
    localizacao_atv = models.CharField(max_length=255, choices=[
        ('interno', 'Interno'),
        ('externo', 'Externo'),
    ])
    prioridade_chamado = models.CharField(max_length=255, choices=[
        ('Alta', 'Alta Prioridade'),
        ('Normal', 'Prioridade Normal'),
        ('Baixa', 'Baixa Prioridade')
    ])
    analista_resp = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='empresas_responsaveis',
        limit_choices_to={'tipo_usuario': 'operador'}
    )
    area_chamado = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True, blank=True)
    tarefa = models.ForeignKey(Tarefa, on_delete=models.SET_NULL, null=True, blank=True, related_name='chamados')
    local_especifico = models.CharField(max_length=255)
    data_criacao = models.DateTimeField(auto_now_add=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='chamados',null=True)
    empresa_nome_fantasia = models.CharField(max_length=255, blank=True)
    empresa_cnpj = models.CharField(max_length=18, blank=True)
    prestadora_servico = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='empresa', null=True, blank=True)
    tecnicos_responsaveis = models.ManyToManyField(Usuario, blank=True, related_name='chamados_tecnicos')
    data_inicio_atv = models.DateTimeField(blank=True, null=True)
    data_fim_atv = models.DateTimeField(blank=True, null=True)
    data_fim_chamado = models.DateTimeField(blank=True, null=True)
    data_limite_atendimento = models.DateTimeField(blank=True, null=True)
    status_chamado = models.CharField(max_length=255,choices=[
        ('aberto', 'Aberto'),
        ('concluido', 'Concluído'),
        ('executando', 'Executando'),
        ('rejeitado', 'Rejeitado'),
        ('assinatura', 'Aguardando assinatura'),
        ('vencidas','OS Vencida')
    ],default='aberto')
    assinatura = models.ImageField(upload_to='signatures/', null=True, blank=True)
    nome_assinante = models.CharField(max_length=255, blank=True)
    email_assinante = models.EmailField(blank=True)
    cargo_assinante = models.CharField(max_length=255, blank=True)
    assinatura_tecnico = models.ImageField(upload_to='signatures/', null=True, blank=True)
    nome_tecnico = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk: 
            prefixo = self.empresa.prefixo
            max_numero = Chamado.objects.filter(
                numero_ordem__startswith=prefixo
            ).aggregate(models.Max('numero_ordem'))['numero_ordem__max']

            if max_numero:
                numero_atual = int(max_numero[len(prefixo):])
                novo_numero = numero_atual + 1
            else:
                novo_numero = 1

            self.numero_ordem = f'{prefixo}{str(novo_numero).zfill(6)}'

        if self.empresa:
            self.empresa_nome_fantasia = self.empresa.nome_fantasia
            self.empresa_cnpj = self.empresa.cnpj
        
        if 'iniciar_atividade' in kwargs:
            self.data_inicio_atv = timezone.now()
        
        if 'fim_atividade' in kwargs:
            self.data_fim_atv = timezone.now()
        
        if not self.data_limite_atendimento:
            try:
                tempo_manutencao = self.empresa.tempos_manutencao.get(tipo_manutencao=self.tipo_manutencao)
                self.data_limite_atendimento = timezone.now() + tempo_manutencao.tempo
            except TempoManutencao.DoesNotExist:
                self.data_limite_atendimento = None  # ou definir um valor padrão
        
        super().save(*args, **kwargs)

    def get_status_chamado_display(self):
        return dict(self._meta.get_field('status_chamado').choices)[self.status_chamado]
    
    def __str__(self):
        return f'Chamado {self.numero_ordem} - {self.titulo}'
    
    
class DetalheTarefaPreenchido(models.Model):
    detalhe_tarefa = models.ForeignKey(DetalheTarefa, on_delete=models.CASCADE)
    chamado = models.ForeignKey(Chamado, on_delete=models.CASCADE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fotos_clientes = models.ImageField(upload_to='fotos_clientes/', blank=True, null=True)
    fotos_ajustes = models.ImageField(upload_to='fotos_ajustes/', blank=True, null=True)
    observacao = models.TextField(blank=True, null=True)
    concluido = models.BooleanField(default=False)
    nao_comporta = models.BooleanField(default=False)

    def __str__(self):
        return f'Detalhe preenchido por {self.usuario} para {self.detalhe_tarefa}'
    

class ImagemChamado(models.Model):
    chamado = models.ForeignKey(Chamado, on_delete=models.CASCADE, related_name='imagens')
    imagem = models.ImageField(upload_to='imagens_chamados/',blank=True, null=True)
    data_upload = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Imagem para o chamado {self.chamado.id}'

class Imagem(models.Model):
    TIPO_IMAGEM_CHOICES = [
        ('cliente', 'Cliente'),
        ('ajuste', 'Ajuste'),
    ]
    
    numero_ordem = models.ForeignKey(Chamado, on_delete=models.CASCADE)
    tarefa = models.ForeignKey(Tarefa, on_delete=models.CASCADE)
    detalhe_tarefa = models.ForeignKey(DetalheTarefaPreenchido, related_name='imagens', on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='imagens_tarefas/')
    tipo_imagem = models.CharField(max_length=10, choices=TIPO_IMAGEM_CHOICES, default='cliente')  # Default set here

    def __str__(self):
        return f"{self.detalhe_tarefa} - {self.tarefa} ({self.numero_ordem.numero_ordem})"


class Chat(models.Model):
    chamado = models.OneToOneField(Chamado, on_delete=models.CASCADE, related_name='chat')

class MensagemChat(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='mensagens')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    conteudo = models.TextField(blank=True)
    imagem = models.ImageField(upload_to='imagens_chat/', blank=True, null=True)
    data_envio = models.DateTimeField(auto_now_add=True)
    empresa = models.ForeignKey(Empresa, null=True, blank=True, on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):
        self.empresa = self.usuario.empresa  
        super().save(*args, **kwargs)