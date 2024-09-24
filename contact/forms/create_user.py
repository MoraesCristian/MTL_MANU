from django import forms
from contact.models import Usuario, Empresa

class UsuarioCreationForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'password', 'empresa', 'telefone', 'tipo_usuario']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'empresa': forms.Select(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_usuario': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        if self.request:
            user = self.request.user
            if user.tipo_usuario == 'manager':
                empresa_choices = [(user.empresa.id, user.empresa.razao_social)]
                self.fields['empresa'].queryset = Empresa.objects.filter(id=user.empresa.id)
            elif user.tipo_usuario == 'user':
                self.fields['empresa'].queryset = Empresa.objects.none()
                
            if user.tipo_usuario == 'manager':
                self.fields['tipo_usuario'].choices = [
                    ('manager', 'Gerente'),
                    ('user', 'Técnico'),
                ]
            elif user.tipo_usuario == 'user':
                self.fields['tipo_usuario'].choices = [
                    ('user', 'Técnico'),
                ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


