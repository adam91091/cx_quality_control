from django import forms

from .models import Client
from ..form_styles import SAP_STYLE, BASIC_REQ_STYLE
from ..user_texts import ERROR_MSG, LABELS, HINTS


class ClientForm(forms.ModelForm):
    """Provide form for client crud operations
    & hint messages for client side validation.
    """
    validation_hints: dict = HINTS['client']

    class Meta:
        model = Client
        exclude = ()

        labels = LABELS['client']

        widgets = {
            'client_sap_id': forms.TextInput(attrs=SAP_STYLE),
            'client_name': forms.TextInput(attrs=BASIC_REQ_STYLE),
        }

        error_messages = ERROR_MSG['client']
