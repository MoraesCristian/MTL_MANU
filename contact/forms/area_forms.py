from django import forms
from contact.models import Area


class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['nome']
