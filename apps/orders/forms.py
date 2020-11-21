from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory, BaseInlineFormSet

from bootstrap_datepicker_plus import DatePickerInput

from apps.form_styles import SAP_STYLE, NUM_STYLE_NO_REQ, BASIC_NO_HINTS_STYLE, INPUT_MEASUREMENT_FORM_STYLE_50px, \
    INPUT_MEASUREMENT_FORM_STYLE_70px, INPUT_MEASUREMENT_FORM_STYLE_71px, ORDER_SAP_STYLE, NUM_STYLE, BASIC_REQ_STYLE, \
    INT_STYLE, PALLET_NUMBER_STYLE
from apps.orders.models import Order, MeasurementReport, Measurement
from apps.user_texts import HINTS, LABELS, ERROR_MSG, FORMSET_MSG
from cx_quality_control.settings import LANGUAGE_CODE


class OrderForm(ModelForm):
    """Provide form for order crud operations
    & hint messages for client side validation.
    """
    validation_hints = HINTS['order']

    class Meta:
        model = Order
        exclude = ('status',)

        labels = LABELS['order']

        widgets = {
            'order_sap_id': forms.TextInput(attrs=ORDER_SAP_STYLE),
            'date_of_production': DatePickerInput(options={'showClear': False, 'locale': LANGUAGE_CODE, },
                                                  attrs=BASIC_REQ_STYLE),
            'product': forms.TextInput(attrs=SAP_STYLE),
            'client': forms.TextInput(attrs=SAP_STYLE),
            'internal_diameter_reference': forms.TextInput(attrs=NUM_STYLE_NO_REQ),
            'external_diameter_reference': forms.TextInput(attrs=NUM_STYLE_NO_REQ),
            'length': forms.TextInput(attrs=NUM_STYLE_NO_REQ),
            'quantity': forms.TextInput(attrs=INT_STYLE),
        }

        error_messages = ERROR_MSG['order']


class MeasurementReportForm(ModelForm):
    """Provide form for measurement report crud operations."""
    class Meta:
        model = MeasurementReport
        exclude = ('order', )

        labels = LABELS['measurement_report']

        widgets = {
            'author': forms.TextInput(attrs=BASIC_REQ_STYLE),
            'date_of_control': DatePickerInput(options={'showClear': False, 'locale': LANGUAGE_CODE, },
                                               attrs=BASIC_REQ_STYLE),
        }


class MeasurementForm(ModelForm):
    """Provide base measurement form used by measurement formset."""
    class Meta:
        model = Measurement
        exclude = ('measurement_report', 'id', )

        labels = LABELS['measurement']

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
                               error=FORMSET_MSG['pallet_number'])
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
