from django import forms
from contact.models import Tarefa, Area, DetalheTarefaPreenchido, Empresa

class TarefaForm(forms.ModelForm):
    empresa = forms.ModelChoiceField(queryset=Empresa.objects.all(), required=True, label="Empresa")

    class Meta:
        model = Tarefa
        fields = ['empresa', 'area', 'descricao']

    def __init__(self, *args, **kwargs):
        super(TarefaForm, self).__init__(*args, **kwargs)
        self.fields['area'].queryset = Area.objects.none()

        if 'empresa' in self.data:
            try:
                empresa_id = int(self.data.get('empresa'))
                self.fields['area'].queryset = Area.objects.filter(empresa_id=empresa_id).order_by('nome')
            except (ValueError, TypeError):
                pass  # ignore invalid input from the client
        elif self.instance.pk:
            self.fields['area'].queryset = self.instance.empresa.area_set.order_by('nome')


class DetalheTarefaPreenchidoForm(forms.ModelForm):
    class Meta:
        model = DetalheTarefaPreenchido
        fields = ['fotos_clientes', 'fotos_ajustes','observacao', 'concluido','nao_comporta']
        widgets = {
            'fotos_clientes': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'fotos_ajustes': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control'}),
            'concluido': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'nao_comporta': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            
        }
        
