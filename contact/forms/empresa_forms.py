from django import forms
from contact.models import Empresa

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = [
            'razao_social', 'nome_fantasia', 'cnpj', 'is_estadual', 'is_municipal', 
            'logradouro', 'estado', 'telefone', 'email_empresa', 'observacao', 'prefixo'
        ]
        widgets = {
            'razao_social': forms.TextInput(attrs={'id': 'razao_social', 'class': 'form-control'}),
            'nome_fantasia': forms.TextInput(attrs={'id': 'nome_fantasia', 'class': 'form-control'}),
            'cnpj': forms.TextInput(attrs={'id': 'cnpj', 'class': 'form-control'}),
            'is_estadual': forms.TextInput(attrs={'id': 'is_estadual', 'class': 'form-control'}),
            'is_municipal': forms.TextInput(attrs={'id': 'is_municipal', 'class': 'form-control'}),
            'logradouro': forms.TextInput(attrs={'id': 'logradouro', 'class': 'form-control'}),
            'estado': forms.Select(attrs={'id': 'estado', 'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'id': 'telefone', 'class': 'form-control'}),
            'email_empresa': forms.EmailInput(attrs={'id': 'email_empresa', 'class': 'form-control'}),
            'observacao': forms.Textarea(attrs={'id': 'observacao', 'class': 'form-control'}),
            'prefixo': forms.TextInput(attrs={'id': 'prefixo', 'class': 'form-control'}),
        }
        

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
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        empresa = super().save(commit=False)
        
        if commit:
            empresa.criado_por = self.request.user
            empresa.save()
        return empresa