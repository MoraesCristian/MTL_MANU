from django import forms
from contact.models import Usuario

class UsuarioCreationForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'password', 'empresa', 'telefone', 'tipo_usuario']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if self.request:
            user = self.request.user
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