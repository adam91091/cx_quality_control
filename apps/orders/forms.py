from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory, BaseInlineFormSet

from bootstrap_datepicker_plus import DatePickerInput

from apps.form_styles import SAP_STYLE, NUM_STYLE_NO_REQ, BASIC_NO_HINTS_STYLE, INPUT_MEASUREMENT_FORM_STYLE_50px, \
    INPUT_MEASUREMENT_FORM_STYLE_70px, INPUT_MEASUREMENT_FORM_STYLE_71px, ORDER_SAP_STYLE, NUM_STYLE, BASIC_REQ_STYLE, \
    INT_STYLE, PALLET_NUMBER_STYLE
from apps.orders.models import Order, MeasurementReport, Measurement


class OrderForm(ModelForm):
    """Provide form for order crud operations
    & hint messages for client side validation.
    """
    validation_hints = {'order_sap_id': "Numer partii musi się składać z 8 cyfr oraz nie może być polem pustym",
                        'product': "Kod produktu musi się składać z 7 cyfr oraz nie może być polem pustym",
                        'client': "Numer SAP klienta musi się składać z 7 cyfr oraz nie może być polem pustym",
                        'date_of_production': 'Pole z datą produkcji nie może być puste',
                        'quantity': 'Podaj całkowitą liczbę tulei w sztukach',
                        }

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
                                                  attrs=BASIC_REQ_STYLE),
            'product': forms.TextInput(attrs=SAP_STYLE),
            'client': forms.TextInput(attrs=SAP_STYLE),
            'internal_diameter_reference': forms.TextInput(attrs=NUM_STYLE_NO_REQ),
            'external_diameter_reference': forms.TextInput(attrs=NUM_STYLE_NO_REQ),
            'length': forms.TextInput(attrs=NUM_STYLE_NO_REQ),
            'quantity': forms.TextInput(attrs=INT_STYLE),
        }

        error_messages = {
            'order_sap_id': {'unique': "Podany nr partii już istnieje.", },
            'product': {'invalid_choice': 'Produkt o podanym nr SAP nie istnieje w bazie danych.', },
            'client': {'invalid_choice': 'Klient o podanym nr SAP nie istnieje w bazie danych.', },
        }


class MeasurementReportForm(ModelForm):
    """Provide form for measurement report crud operations."""
    class Meta:
        model = MeasurementReport
        exclude = ('order',)
        labels = {
            'author': "Kontrolował",
            'date_of_control': "Data kontroli",
        }
        widgets = {
            'author': forms.TextInput(attrs=BASIC_REQ_STYLE),
            'date_of_control': DatePickerInput(options={'showClear': False, 'locale': 'pl', },
                                               attrs=BASIC_REQ_STYLE),
        }


class MeasurementForm(ModelForm):
    """Provide base measurement form used by measurement formset."""
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
                                                    **PALLET_NUMBER_STYLE}),
            'internal_diameter_tolerance_top': forms.TextInput(attrs={**INPUT_MEASUREMENT_FORM_STYLE_50px,
                                                                      **NUM_STYLE}),
            'internal_diameter_target': forms.TextInput(attrs={**INPUT_MEASUREMENT_FORM_STYLE_50px,
                                                               **NUM_STYLE}),
            'internal_diameter_tolerance_bottom': forms.TextInput(attrs={**INPUT_MEASUREMENT_FORM_STYLE_50px,
                                                                         **NUM_STYLE}),
            'external_diameter_tolerance_top': forms.TextInput(attrs={**INPUT_MEASUREMENT_FORM_STYLE_50px,
                                                                      **NUM_STYLE}),
            'external_diameter_target': forms.TextInput(attrs={**INPUT_MEASUREMENT_FORM_STYLE_50px,
                                                               **NUM_STYLE}),
            'external_diameter_tolerance_bottom': forms.TextInput(attrs={**INPUT_MEASUREMENT_FORM_STYLE_50px,
                                                                         **NUM_STYLE}),
            'length_tolerance_top': forms.TextInput(attrs={**INPUT_MEASUREMENT_FORM_STYLE_50px,
                                                    **NUM_STYLE}),
            'length_target': forms.TextInput(attrs={**INPUT_MEASUREMENT_FORM_STYLE_50px,
                                                    **NUM_STYLE}),
            'length_tolerance_bottom': forms.TextInput(attrs={**INPUT_MEASUREMENT_FORM_STYLE_50px,
                                                              **NUM_STYLE}),
            'flat_crush_resistance_target': forms.TextInput(attrs={**INPUT_MEASUREMENT_FORM_STYLE_70px,
                                                                   **BASIC_NO_HINTS_STYLE}),
            'moisture_content_target': forms.TextInput(attrs={**INPUT_MEASUREMENT_FORM_STYLE_50px,
                                                              **BASIC_NO_HINTS_STYLE}),
            'weight': forms.TextInput(attrs={**INPUT_MEASUREMENT_FORM_STYLE_50px, **BASIC_NO_HINTS_STYLE}),
            'remarks': forms.TextInput(attrs={**INPUT_MEASUREMENT_FORM_STYLE_71px, **BASIC_NO_HINTS_STYLE}),
        }


class MeasurementInlineFormSet(BaseInlineFormSet):
    """Measurement inline formset customization."""
    def is_valid(self) -> bool:
        """Extend all measurement form validation for
        pallet number uniqueness check.
        """
        if not self.check_pallet_uniqueness():
            for form in self.forms[:1]:
                form.add_error(field='pallet_number',
                               error="Numery palet nie mogą się powtarzać w raporcie pomiarowym!")
            return False
        return super().is_valid()

    def check_pallet_uniqueness(self) -> bool:
        """Verify if pallet numbers collection contains unique values."""
        pallet_nums = [form['pallet_number'].value() for form in self.forms]
        return len(set(pallet_nums)) == len(pallet_nums)


MeasurementFormSet = inlineformset_factory(parent_model=MeasurementReport, model=Measurement,
                                           form=MeasurementForm, extra=0, min_num=1, formset=MeasurementInlineFormSet)


class DateFilteringForm(forms.Form):
    """Helper form for date filter."""
    date_of_production_after = forms.DateField(
        widget=DatePickerInput(options={'showClear': False, 'locale': 'pl', },
                               attrs={**BASIC_NO_HINTS_STYLE, **{'name': 'date_of_production_after',
                                                                 'id': 'id_date_of_production_0'}},
                               format='%Y-%m-%d'), label='Od')

    date_of_production_before = forms.DateField(
        widget=DatePickerInput(options={'showClear': False, 'locale': 'pl', },
                               attrs={**BASIC_NO_HINTS_STYLE, **{'name': 'date_of_production_before',
                                                                 'id': 'id_date_of_production_1'}},
                               format='%Y-%m-%d'), label='Do')
