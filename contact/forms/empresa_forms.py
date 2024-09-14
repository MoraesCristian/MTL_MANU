from django import forms
from contact.models import Empresa

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['razao_social', 'nome_fantasia', 'cnpj', 'is_estadual', 'is_municipal', 'logradouro', 'estado', 'telefone', 'email_empresa', 'observacao', 'prefixo']
        

class AdicionarEmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['razao_social', 'nome_fantasia', 'cnpj', 'is_estadual', 'is_municipal', 'logradouro', 'estado', 'telefone', 'email_empresa', 'observacao', 'prefixo']
        widgets = {
            'razao_social': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_fantasia': forms.TextInput(attrs={'class': 'form-control'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control'}),
            'is_estadual': forms.TextInput(attrs={'class': 'form-control'}),
            'is_municipal': forms.TextInput(attrs={'class': 'form-control'}),
            'logradouro': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'email_empresa': forms.EmailInput(attrs={'class': 'form-control'}),
            'observacao': forms.TextInput(attrs={'class': 'form-control'}),
            'prefixo': forms.TextInput(attrs={'class': 'form-control'}),
        }
