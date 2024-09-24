from django import forms
from contact.models import Chamado, Tarefa, Empresa, Usuario,  MensagemChat, DetalheTarefa

class ChamadoForm(forms.ModelForm):
    empresa_nome_fantasia = forms.ModelChoiceField(
        queryset=Empresa.objects.none(),  # Inicialmente vazio
        required=True,
        label='Empresa'
    )
    prestadora_servico = forms.ModelChoiceField(
        queryset=Empresa.objects.none(),  # Inicialmente vazio
        required=False,
        label='Terceiro'
    )
    tecnico_responsavel = forms.ModelChoiceField(
        queryset=Usuario.objects.none(),  # Substitua com o modelo de usuário ou técnico apropriado
        required=False,
        label='Técnico Responsável'
    )

    class Meta:
        model = Chamado
        fields = [
            'empresa_nome_fantasia', 'localizacao_atv', 'tipo_manutencao',
            'area_chamado', 'tarefa', 'descricao', 'local_especifico',
            'prioridade_chamado', 'prestadora_servico', 'tecnico_responsavel'
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
            'prestadora_servico': forms.Select(attrs={'required': True}),
            'tecnico_responsavel': forms.Select(attrs={'required': True}),
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

        # TAREFA DROP DOWN DINAMICO
        self.fields['tarefa'].queryset = Tarefa.objects.none()

        # Definindo as opções da área do chamado
        self.fields['area_chamado'].choices = [('', 'Selecione a área')] + list(self.fields['area_chamado'].choices)
                
        if 'area_chamado' in self.data:
            try:
                area_id = int(self.data.get('area_chamado'))
                self.fields['tarefa'].queryset = Tarefa.objects.filter(area_id=area_id)
            except (ValueError, TypeError):
                    pass
        elif self.instance.pk:
            self.fields['tarefa'].queryset = self.instance.area_chamado.tarefas.all()


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
