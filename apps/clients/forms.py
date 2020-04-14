from django import forms

from .models import Client
from ..forms_utils import SAP_STYLE, BASIC_REQ_STYLE


class ClientForm(forms.ModelForm):

    validation_hints = {'client_sap_id': "Numer SAP musi się składać z 6 cyfr oraz nie może być polem pustym",
                        'client_name': "Pole z nazwą klienta nie może być puste"}

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
