from django import forms
from contact.models import Chamado

class ChamadoForm(forms.ModelForm):
    class Meta:
        model = Chamado
        fields = ['empresa', 'localizacao_atv', 'tipo_manutencao', 'area', 'descricao']
