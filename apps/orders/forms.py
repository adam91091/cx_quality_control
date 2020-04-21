import datetime as dt

from django import forms
from django.forms import ModelForm

from bootstrap_datepicker_plus import DatePickerInput

from apps.forms_utils import SAP_STYLE, NUM_STYLE_NO_REQ, BASIC_NO_HINTS_STYLE
from apps.orders.models import Order

STRFTIME_STRING = '%Y-%m-%d 00:00:00'


class OrderForm(ModelForm):
    validation_hints = {'order_sap_id': "Numer partii musi się składać z 6 cyfr oraz nie może być polem pustym",
                        'product': "Kod produktu musi się składać z 6 cyfr oraz nie może być polem pustym",
                        'client': "Numer SAP klienta musi się składać z 6 cyfr oraz nie może być polem pustym",
                        }

    def __init__(self, read_only=False, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        if read_only:
            for field in self.fields.values():
                field.widget.attrs['readonly'] = True
                field.widget.attrs['disabled'] = 'true'

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
            'date_of_production': DatePickerInput(options={'minDate': (dt.datetime.today()).strftime(STRFTIME_STRING),
                                                           'showClear': False, 'locale': 'pl', },
                                                  attrs=BASIC_NO_HINTS_STYLE),
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