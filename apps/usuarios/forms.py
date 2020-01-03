from django import forms
from apps.usuarios.models import Perfil

class ProfileForm(forms.Form):
    #report_body_font = forms.CharField(widget=forms.HiddenInput)

    class Meta:
        model = Perfil
        fields= [
            'user',
            'report_body_font',
        ]