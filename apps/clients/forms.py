from django import forms

from .models import Client
from ..form_styles import SAP_STYLE, BASIC_REQ_STYLE


class ClientForm(forms.ModelForm):

    validation_hints = {'client_sap_id': "Numer SAP musi się składać z 7 cyfr oraz nie może być polem pustym",
                        'client_name': "Pole z nazwą klienta nie może być puste"}

    def __init__(self, read_only=False, update=False, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        if read_only:
            for field_name in self.fields:
                self.fields[field_name].disabled = True
        if update:
            self.fields['client_sap_id'].disabled = True

    class Meta:
        model = Client
        exclude = ()
        labels = {
            'client_sap_id': "Numer SAP klienta",
            'client_name': "Nazwa klienta",
        }
        widgets = {
            'client_sap_id': forms.TextInput(attrs=SAP_STYLE),
            'client_name': forms.TextInput(attrs=BASIC_REQ_STYLE),
        }

        error_messages = {
            'client_sap_id': {'unique': "Klient o podanym numerze SAP już istnieje.", }
        }
