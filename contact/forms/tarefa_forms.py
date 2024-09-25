from django import forms
from contact.models import Tarefa, Area, DetalheTarefaPreenchido

class TarefaForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = ['area', 'descricao']
        widgets = {
            'area': forms.Select(attrs={'required': True}),
            'descricao': forms.TextInput(attrs={'required': True}),
        }


class DetalheTarefaPreenchidoForm(forms.ModelForm):
    class Meta:
        model = DetalheTarefaPreenchido
        fields = ['fotos_clientes', 'fotos_ajustes', 'observacao', 'concluido']
        widgets = {
            'observacao': forms.Textarea(attrs={'rows': 4}),
            'concluido': forms.CheckboxInput(),
        }