from django import forms
from contact.models import Usuario, Empresa

class UsuarioCreationForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'password', 'empresa', 'telefone', 'tipo_usuario', 'cpf']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
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
                self.fields['empresa'].queryset = Empresa.objects.filter(id=user.empresa.id)
            elif user.tipo_usuario == 'user':
                self.fields['empresa'].queryset = Empresa.objects.none()
                
            if user.tipo_usuario == 'admin':
                self.fields['tipo_usuario'].choices = [
                    ('admin', 'Administrador'),
                    ('operador', 'Operador'),
                    ('manager', 'Cliente'),
                    ('user', 'Terceiro'),
                ]
            elif user.tipo_usuario == 'operador':
                self.fields['tipo_usuario'].choices = [
                    ('operador', 'Operador'),
                    ('manager', 'Cliente'),
                    ('user', 'Terceiro'),
                ]
            else:
                self.fields['tipo_usuario'].choices = []

    def clean(self):
        cleaned_data = super().clean()
        tipo_usuario = cleaned_data.get('tipo_usuario')
        cpf = cleaned_data.get('cpf')

        if tipo_usuario == 'user' and not cpf:
            self.add_error('cpf', 'O campo CPF é obrigatório para o tipo de usuário "Tecnico".')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
