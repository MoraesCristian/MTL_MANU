from django import forms
from contact.models import Chamado, Tarefa, Empresa, Usuario,  MensagemChat, DetalheTarefa, ImagemChamado


class ChamadoForm(forms.ModelForm):
    empresa_nome_fantasia = forms.ModelChoiceField(
        queryset=Empresa.objects.none(),  # Inicialmente vazio
        required=True,
        label='Empresa'
    )
    prestadora_servico = forms.ModelChoiceField(
        queryset=Empresa.objects.all(),  # Mostrar todas as empresas
        required=False,
        label='Terceiro'
    )
    tecnico_responsavel = forms.ModelChoiceField(
        queryset=Usuario.objects.none(),  # Substitua com o modelo de usuário ou técnico apropriado
        required=False,
        label='Técnico Responsável'
    )
    imagens = forms.FileField(
        required=False, 
        label='Imagens'
    )
     
    class Meta:
        model = Chamado
        fields = [
            'empresa_nome_fantasia', 'localizacao_atv', 'tipo_manutencao',
            'area_chamado', 'tarefa', 'descricao', 'local_especifico',
            'prioridade_chamado', 'prestadora_servico', 'tecnico_responsavel',
            'imagens'
        ]
        widgets = {
            'empresa_nome_fantasia': forms.Select(attrs={'required': True}),
            'localizacao_atv': forms.Select(attrs={'required': True}),
            'tipo_manutencao': forms.Select(attrs={'required': True}),
            'area_chamado': forms.Select(attrs={'required': True}),
            'tarefa': forms.Select(attrs={'required': True}),
            'descricao': forms.Textarea(attrs={'required': True}),
            'local_especifico': forms.TextInput(attrs={'required': True}),
            'prioridade_chamado': forms.Select(attrs={'required': True}),
            'prestadora_servico': forms.Select(attrs={'required': False}),
            'imagens': forms.ClearableFileInput(attrs={'required': False}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        empresas = kwargs.pop('empresas', None)
        super().__init__(*args, **kwargs)
        
        if empresas is not None:
            self.fields['empresa_nome_fantasia'].queryset = empresas
            self.fields['empresa_nome_fantasia'].label_from_instance = lambda obj: obj.nome_fantasia

        if user and user.is_superuser:
            self.fields['empresa_nome_fantasia'].required = False
        else:
            self.fields['empresa_nome_fantasia'].required = True

        self.fields['tarefa'].queryset = Tarefa.objects.none()
        
        self.fields['area_chamado'].choices = [('', 'Selecione a área')] + list(self.fields['area_chamado'].choices)[1:]

        if 'area_chamado' in self.data:
            try:
                area_id = int(self.data.get('area_chamado'))
                self.fields['tarefa'].queryset = Tarefa.objects.filter(area_id=area_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['tarefa'].queryset = self.instance.area_chamado.tarefas.all()

class AssinaturaForm(forms.ModelForm):
    nome_assinante = forms.CharField(
        required=True,
        label='Nome do Assinante',
        widget=forms.TextInput(attrs={'required': True})
    )
    email_assinante = forms.EmailField(
        required=True,
        label='Email do Assinante',
        widget=forms.EmailInput(attrs={'required': True})
    )
    assinatura = forms.ImageField(
        required=True,
        label='Assinatura',
        widget=forms.ClearableFileInput(attrs={'required': True})
    )

    class Meta:
        model = Chamado
        fields = ['nome_assinante', 'email_assinante', 'assinatura']


class ImagemChamadoForm(forms.ModelForm):
    class Meta:
        model = ImagemChamado
        fields = ['imagem']
        widgets = {
            'imagem': forms.ClearableFileInput({'class': 'form-control-file'}),
        }
class MensagemChatForm(forms.ModelForm):
    class Meta:
        model = MensagemChat
        fields = ['conteudo']
        widgets = {
            'conteudo': forms.Textarea(attrs={'rows': 2, 'cols': 40})
        }
        

class DetalheTarefaForm(forms.ModelForm):
    tarefa = forms.ModelChoiceField(queryset=Tarefa.objects.none(), widget=forms.HiddenInput())

    class Meta:
        model = DetalheTarefa
        fields = ['tarefa', 'descricao']

    def __init__(self, *args, **kwargs):
        tarefa = kwargs.pop('tarefa', None)
        super().__init__(*args, **kwargs)
        if tarefa:
            self.fields['tarefa'].queryset = Tarefa.objects.filter(id=tarefa.id)
            self.fields['tarefa'].initial = tarefa

class AdicionarPrestadoraServicoForm(forms.ModelForm):
    prestadora_servico = forms.ModelChoiceField(
        queryset=Empresa.objects.all(),
        required=True,
        label='Prestadora de Serviço'
    )

    class Meta:
        model = Chamado
        fields = ['prestadora_servico']