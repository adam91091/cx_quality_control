from django import forms

from .models import Client


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        exclude = ()
        labels = {
            'client_sap_id': "Numer SAP klienta",
            'client_name': "Nazwa klienta",
        }
        widgets = {
            'client_sap_id': forms.TextInput(attrs={'class': 'form-control'}),
            'client_name': forms.TextInput(attrs={'class': 'form-control'}),
        }