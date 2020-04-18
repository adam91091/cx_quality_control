from django import forms
from django.forms import ModelForm

from apps.clients.models import Client
from apps.forms_utils import NUM_STYLE, INT_STYLE, BASIC_REQ_STYLE, BASIC_STYLE, BASIC_NO_HINTS_STYLE, SAP_STYLE, \
    NUM_STYLE_NO_REQ, DATE_STYLE
from apps.orders.models import Order, MeasurementReport, Measurement
from apps.products.models import Product


class OrderForm(ModelForm):
    validation_hints = {'order_sap_id': "Numer partii musi się składać z 6 cyfr oraz nie może być polem pustym",
                        'product': "Kod produktu musi się składać z 6 cyfr oraz nie może być polem pustym",
                        'client': "Numer SAP klienta musi się składać z 6 cyfr oraz nie może być polem pustym",
                        'date_of_production': "Data produkcji musi być w formacie dd.mm.rrrr oraz nie może być "
                                              "wcześniejsa od dzisiejszej"
                        }

    class Meta:
        model = Order
        exclude = ('status', )
        labels = {
            'order_sap_id': "Nr partii",
            'date_of_production': "Data produkcji",
            'product': "Kod produktu",
            'client': "Nr sap klienta",
            'internal_diameter_reference': "Średnica wewnętrzna",
            'external_diameter_reference': "Średnica zewnętrzna",
            'length': "Długość",
            'quantity': "Ilość",
        }
        widgets = {
            'order_sap_id': forms.TextInput(attrs=SAP_STYLE),
            'date_of_production': forms.DateInput(attrs=DATE_STYLE, format='%d.%m.%Y'),
            'product': forms.TextInput(attrs=SAP_STYLE),
            'client': forms.TextInput(attrs=SAP_STYLE),
            'internal_diameter_reference': forms.TextInput(attrs=NUM_STYLE_NO_REQ),
            'external_diameter_reference': forms.TextInput(attrs=NUM_STYLE_NO_REQ),
            'length': forms.TextInput(attrs=NUM_STYLE_NO_REQ),
            'quantity': forms.TextInput(attrs=NUM_STYLE_NO_REQ),
        }

        error_messages = {
            'order_sap_id': {'unique': "Podany nr partii już istnieje.", }
        }


class MeasurementReportForm(ModelForm):
    pass


class MeasurementForm(ModelForm):
    pass
