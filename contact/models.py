
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings

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
        ('manager', 'Gerente'),
        ('user', 'Técnico'),]
    id = models.AutoField(primary_key=True) 
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE, null=True, blank=True)
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
        return self.tipo_usuario in ['admin', 'manager']

    def can_create_admin(self):
        return self.tipo_usuario == 'admin'

    def can_create_manager(self):
        return self.tipo_usuario in ['admin', 'manager']
    
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

    def __str__(self):
        return self.razao_social

class Chamado(models.Model):
    id = models.AutoField(primary_key=True)
    numero_ordem = models.CharField(max_length=20, unique=True, editable=False)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    descricao = models.TextField(blank=True)
    tipo_manutencao = models.CharField(max_length=255, choices=[
        ('preventiva', 'preventiva'),
        ('emergial', 'emergial'),
        ('corretiva', 'corretiva'),
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
    local_especifico = models.CharField(max_length=255)
    data_criacao = models.DateTimeField(auto_now_add=True)
    empresa_nome_fantasia = models.CharField(max_length=255, blank=True)
    empresa_cnpj = models.CharField(max_length=18, blank=True)
    usuario_telefone = models.CharField(max_length=50, blank=True)
    data_inicio_atv = models.DateTimeField(blank=True, null=True)
    data_fim_atv = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk: 
            prefixo = self.usuario.empresa.prefixo
            max_numero = Chamado.objects.filter(
                numero_ordem__startswith=prefixo
            ).aggregate(models.Max('numero_ordem'))['numero_ordem__max']

            if max_numero:
                numero_atual = int(max_numero[len(prefixo):]) 
                novo_numero = numero_atual + 1
            else:
                novo_numero = 1

            self.numero_ordem = f'{prefixo}{str(novo_numero).zfill(6)}'
        if self.usuario:
            self.empresa_nome_fantasia = self.usuario.empresa.nome_fantasia
            self.empresa_cnpj = self.usuario.empresa.cnpj
            self.usuario_telefone = self.usuario.telefone
            self.usuario_first_name = self.usuario.first_name
            self.usuario_last_name = self.usuario.last_name
        
        if 'iniciar_atividade' in kwargs:
            self.data_inicio_atv = timezone.now()
        
        if 'fim_atividade' in kwargs:
            self.data_fim_atv = timezone.now()
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Chamado {self.numero_ordem} - {self.titulo}'

    def get_usuario_nome(self):
        return f'{self.usuario.first_name} {self.usuario.last_name}'

class ImagemChamado(models.Model):
    chamado = models.ForeignKey('Chamado', on_delete=models.CASCADE, related_name='imagens')
    numero_ordem = models.CharField(max_length=20)
    tipo_imagem = models.CharField(max_length=50, choices=[
        ('antes', 'Antes'),
        ('depois', 'Depois'),
    ])
    imagem_cliente_operador = models.ImageField(upload_to='fotos_Abertura/%Y/%m/%d')
    imagem_prestador = models.ImageField(upload_to='fotos_fechamento/%Y/%m/%d/', blank=True, null=True)
    data_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.numero_ordem} - {self.tipo_imagem}'
