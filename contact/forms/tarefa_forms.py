from django import forms
from contact.models import Tarefa, Area

class TarefaForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = ['area', 'descricao']
        widgets = {
            'area': forms.Select(attrs={'required': True}),
            'descricao': forms.TextInput(attrs={'required': True}),
        }
