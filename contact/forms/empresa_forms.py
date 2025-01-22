from django import forms
from django.forms.models import inlineformset_factory
from contact.models import Empresa, TempoManutencao, DocumentoEmpresa, Usuario



class EmpresaForm(forms.ModelForm):
    tempo_preventiva = forms.DurationField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex:: 4:00:00 para 4 horas, 2 days para 2 dias'})
    )
    tempo_emergencial = forms.DurationField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex:: 4:00:00 para 4 horas, 2 days para 2 dias'})
    )
    tempo_corretiva = forms.DurationField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex:: 4:00:00 para 4 horas, 2 days para 2 dias'})
    )

    class Meta:
        model = Empresa
        fields = [
            'razao_social', 'nome_fantasia', 'cnpj', 'is_estadual', 'is_municipal',
            'logradouro', 'estado', 'telefone', 'email_empresa', 'observacao', 'prefixo',
            'filial_de', 'tempo_preventiva', 'tempo_emergencial', 'tempo_corretiva',
            'responsavel_empre', 'email_responsavel','analista_resp',
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
            'filial_de': forms.Select(attrs={'id': 'filial_de', 'class': 'form-control'}),
            'responsavel_empre': forms.TextInput(attrs={'class': 'form-control'}),
            'email_responsavel': forms.EmailInput(attrs={'class': 'form-control'}),
            'analista_resp': forms.Select(attrs={'class': 'form-control'}), 
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['analista_resp'].queryset = Usuario.objects.filter(tipo_usuario='operador')
        
        if self.instance.pk:
            try:
                tempo = TempoManutencao.objects.get(empresa=self.instance, tipo_manutencao='preventiva')
                self.fields['tempo_preventiva'].initial = tempo.tempo
            except TempoManutencao.DoesNotExist:
                pass
            try:
                tempo = TempoManutencao.objects.get(empresa=self.instance, tipo_manutencao='emergencial')
                self.fields['tempo_emergencial'].initial = tempo.tempo
            except TempoManutencao.DoesNotExist:
                pass
            try:
                tempo = TempoManutencao.objects.get(empresa=self.instance, tipo_manutencao='corretiva')
                self.fields['tempo_corretiva'].initial = tempo.tempo
            except TempoManutencao.DoesNotExist:
                pass

    def save(self, commit=True):
        empresa = super().save(commit=False)

        if commit:
            empresa.save()
            TempoManutencao.objects.update_or_create(
                empresa=empresa,
                tipo_manutencao='preventiva',
                defaults={'tempo': self.cleaned_data.get('tempo_preventiva')}
            )
            TempoManutencao.objects.update_or_create(
                empresa=empresa,
                tipo_manutencao='emergencial',
                defaults={'tempo': self.cleaned_data.get('tempo_emergencial')}
            )
            TempoManutencao.objects.update_or_create(
                empresa=empresa,
                tipo_manutencao='corretiva',
                defaults={'tempo': self.cleaned_data.get('tempo_corretiva')}
            )

        return empresa

class AdicionarEmpresaForm(forms.ModelForm):
    tempo_preventiva = forms.DurationField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 4:00:00 para 4 horas, 2 days para 2 dias'})
    )
    tempo_emergencial = forms.DurationField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 4:00:00 para 4 horas, 2 days para 2 dias'})
    )
    tempo_corretiva = forms.DurationField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex:: 4:00:00 para 4 horas, 2 days para 2 dias'})
    )

    class Meta:
        model = Empresa
        fields = [
            'razao_social', 'nome_fantasia', 'cnpj', 'is_estadual', 'is_municipal', 'logradouro',
            'estado', 'telefone', 'email_empresa', 'observacao', 'prefixo', 'filial_de', 'responsavel_empre',
            'email_responsavel', 'analista_resp',
        ]
        
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
            'filial_de': forms.Select(attrs={'id': 'filial_de', 'class': 'form-control'}),
            'responsavel_empre': forms.TextInput(attrs={'class': 'form-control'}),
            'email_responsavel': forms.EmailInput(attrs={'class': 'form-control'}),
            'analista_resp': forms.Select(attrs={'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        self.fields['analista_resp'].queryset = Usuario.objects.filter(tipo_usuario='operador')

    def save(self, commit=True):
        empresa = super().save(commit=False)
        
        if commit:
            empresa.criado_por = self.request.user
            empresa.save()
            
            TempoManutencao.objects.update_or_create(
                empresa=empresa,
                tipo_manutencao='preventiva',
                defaults={'tempo': self.cleaned_data.get('tempo_preventiva')}
            )
            TempoManutencao.objects.update_or_create(
                empresa=empresa,
                tipo_manutencao='emergencial',
                defaults={'tempo': self.cleaned_data.get('tempo_emergencial')}
            )
            TempoManutencao.objects.update_or_create(
                empresa=empresa,
                tipo_manutencao='corretiva',
                defaults={'tempo': self.cleaned_data.get('tempo_corretiva')}
            )

        return empresa
    
class TempoManutencaoForm(forms.ModelForm):
    class Meta:
        model = TempoManutencao
        fields = ['tipo_manutencao', 'tempo']
        widgets = {
            'tipo_manutencao': forms.Select(attrs={'class': 'form-control'}),
            'tempo': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
class DocumentoForm(forms.ModelForm):
    class Meta:
        model = DocumentoEmpresa
        fields = ['tipo_documento', 'descricao', 'documento']
        widgets = {
            'tipo_documento': forms.Select(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'documento': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
