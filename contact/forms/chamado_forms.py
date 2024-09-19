from django import forms
from contact.models import Chamado, Tarefa, Empresa

class ChamadoForm(forms.ModelForm):
    empresa_nome_fantasia = forms.ModelChoiceField(
        queryset=Empresa.objects.none(),  # Inicialmente vazio
        required=True,
        label='Empresa'
    )
    class Meta:
        model = Chamado
        fields = [
            'empresa_nome_fantasia', 'localizacao_atv', 'tipo_manutencao',
            'area_chamado', 'tarefa', 'descricao', 'local_especifico'
        ]
        widgets = {
            'empresa_nome_fantasia': forms.Select(attrs={'required': True}),
            'localizacao_atv': forms.Select(attrs={'required': True}),
            'tipo_manutencao': forms.Select(attrs={'required': True}),
            'area_chamado': forms.Select(attrs={'required': True}),
            'tarefa': forms.Select(attrs={'required': True}),
            'descricao': forms.Textarea(attrs={'required': True}),
            'local_especifico': forms.TextInput(attrs={'required': True}),
        }

    def __init__(self, *args, **kwargs):
        # Adiciona a lista de empresas ao formulário
        empresas = kwargs.pop('empresas', Empresa.objects.none())
        super().__init__(*args, **kwargs)
        self.fields['empresa_nome_fantasia'].queryset = empresas
        
        # Ajusta o queryset do campo 'empresa_nome_fantasia' baseado no tipo de usuário
        
        self.fields['tarefa'].queryset = Tarefa.objects.none()
        
        if 'area_chamado' in self.data:
            try:
                area = self.data.get('area_chamado')
                self.fields['tarefa'].queryset = Tarefa.objects.filter(area=area)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['tarefa'].queryset = self.instance.tarefa_set.all()