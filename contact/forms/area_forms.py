from django import forms
from contact.models import Area


class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['nome', 'empresa']
        widgets = {
            'empresa': forms.Select(attrs={'class': 'form-control'})
        }