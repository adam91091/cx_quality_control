from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from bootstrap_datepicker_plus import DatePickerInput

from apps.forms_utils import SAP_STYLE, NUM_STYLE_NO_REQ, BASIC_NO_HINTS_STYLE, INPUT_MEASUREMENT_FORM_STYLE_50px, \
    INPUT_MEASUREMENT_FORM_STYLE_70px, INPUT_MEASUREMENT_FORM_STYLE_71px, ORDER_SAP_STYLE
from apps.orders.models import Order, MeasurementReport, Measurement

STRFTIME_STRING = '%Y-%m-%d 00:00:00'


class OrderForm(ModelForm):
    validation_hints = {'order_sap_id': "Numer partii musi się składać z 8 cyfr oraz nie może być polem pustym",
                        'product': "Kod produktu musi się składać z 7 cyfr oraz nie może być polem pustym",
                        'client': "Numer SAP klienta musi się składać z 7 cyfr oraz nie może być polem pustym",
                        }

    def __init__(self, read_only=False, measurement_report=False, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        if read_only:
            for field in self.fields.values():
                field.widget.attrs['readonly'] = True
                field.widget.attrs['disabled'] = 'true'
        elif measurement_report:
            for field in self.fields:
                self.fields[field].widget.attrs['readonly'] = True

    class Meta:
        model = Order
        exclude = ('status',)
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
            'order_sap_id': forms.TextInput(attrs=ORDER_SAP_STYLE),
            'date_of_production': DatePickerInput(options={'showClear': False, 'locale': 'pl', },
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
    def __init__(self, read_only=False, *args, **kwargs):
        super(MeasurementReportForm, self).__init__(*args, **kwargs)
        if read_only:
            for field_name in self.fields:
                self.fields[field_name].disabled = True

    class Meta:
        model = MeasurementReport
        exclude = ('order',)
        labels = {
            'author': "Kontrolował",
            'date_of_control': "Data",
        }
        widgets = {
            'author': forms.TextInput(attrs=BASIC_NO_HINTS_STYLE),
            'date_of_control': DatePickerInput(options={'showClear': False, 'locale': 'pl', },
                                               attrs=BASIC_NO_HINTS_STYLE),
        }


class MeasurementForm(ModelForm):
    class Meta:
        model = Measurement
        exclude = ('measurement_report', 'id')
        labels = {
            'pallet_number': "Paleta nr",
            'internal_diameter_tolerance_top': "Góra",
            'internal_diameter_target': "Środek",
            'internal_diameter_tolerance_bottom': "Dół",
            'external_diameter_tolerance_top': "Góra",
            'external_diameter_target': "Środek",
            'external_diameter_tolerance_bottom': "Dół",
            'length_tolerance_top': "Góra",
            'length_target': "Środek",
            'length_tolerance_bottom': "Dół",
            'flat_crush_resistance_target': "Kontrola wytrzymałości",
            'moisture_content_target': "Wilgotność",
            'weight': "Waga",
            'remarks': 'Uwagi, klejenie, pakowanie',
        }
        widgets = {
            'pallet_number': forms.TextInput(attrs={**INPUT_MEASUREMENT_FORM_STYLE_50px,
                                                    **BASIC_NO_HINTS_STYLE}),
            'internal_diameter_tolerance_top': forms.TextInput(attrs={**INPUT_MEASUREMENT_FORM_STYLE_50px,
                                                                      **BASIC_NO_HINTS_STYLE}),
            'internal_diameter_target': forms.TextInput(attrs={**INPUT_MEASUREMENT_FORM_STYLE_50px,
                                                               **BASIC_NO_HINTS_STYLE}),
            'internal_diameter_tolerance_bottom': forms.TextInput(attrs={**INPUT_MEASUREMENT_FORM_STYLE_50px,
                                                                         **BASIC_NO_HINTS_STYLE}),
            'external_diameter_tolerance_top': forms.TextInput(attrs={**INPUT_MEASUREMENT_FORM_STYLE_50px,
                                                                      **BASIC_NO_HINTS_STYLE}),
            'external_diameter_target': forms.TextInput(attrs={**INPUT_MEASUREMENT_FORM_STYLE_50px,
                                                               **BASIC_NO_HINTS_STYLE}),
            'external_diameter_tolerance_bottom': forms.TextInput(attrs={**INPUT_MEASUREMENT_FORM_STYLE_50px,
                                                                         **BASIC_NO_HINTS_STYLE}),
            'length_tolerance_top': forms.TextInput(attrs={**INPUT_MEASUREMENT_FORM_STYLE_50px,
                                                    **BASIC_NO_HINTS_STYLE}),
            'length_target': forms.TextInput(attrs={**INPUT_MEASUREMENT_FORM_STYLE_50px,
                                                    **BASIC_NO_HINTS_STYLE}),
            'length_tolerance_bottom': forms.TextInput(attrs={**INPUT_MEASUREMENT_FORM_STYLE_50px,
                                                              **BASIC_NO_HINTS_STYLE}),
            'flat_crush_resistance_target': forms.TextInput(attrs={**INPUT_MEASUREMENT_FORM_STYLE_70px,
                                                                   **BASIC_NO_HINTS_STYLE}),
            'moisture_content_target': forms.TextInput(attrs={**INPUT_MEASUREMENT_FORM_STYLE_50px,
                                                              **BASIC_NO_HINTS_STYLE}),
            'weight': forms.TextInput(attrs={**INPUT_MEASUREMENT_FORM_STYLE_50px, **BASIC_NO_HINTS_STYLE}),
            'remarks': forms.TextInput(attrs={**INPUT_MEASUREMENT_FORM_STYLE_71px, **BASIC_NO_HINTS_STYLE}),
        }

    @staticmethod
    def make_form_readonly(form):
        for field_name in form.fields:
            form.fields[field_name].disabled = True


MeasurementFormSet = inlineformset_factory(parent_model=MeasurementReport, model=Measurement,
                                           form=MeasurementForm, extra=0, min_num=1)


class DateFilteringForm(forms.Form):
    search_start_date = forms.DateField(
        widget=DatePickerInput(options={'showClear': False, 'locale': 'pl', },
                               attrs=BASIC_NO_HINTS_STYLE, format='%Y-%m-%d'), label='Od')
    search_end_date = forms.DateField(
        widget=DatePickerInput(options={'showClear': False, 'locale': 'pl', },
                               attrs=BASIC_NO_HINTS_STYLE, format='%Y-%m-%d'), label='Do')
