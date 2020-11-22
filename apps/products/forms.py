from betterforms.multiform import MultiModelForm
from bootstrap_datepicker_plus import DatePickerInput
from django import forms

from apps.form_styles import NUM_STYLE, INT_STYLE, BASIC_REQ_STYLE, BASIC_STYLE, BASIC_NO_HINTS_STYLE, SAP_STYLE
from apps.products.models import Product, Specification
from apps.user_texts import HINTS, LABELS, ERROR_MSG


class ProductForm(forms.ModelForm):
    """Provide form for product crud operations
    & hint messages for client side validation.
    """
    validation_hints: dict = HINTS['product']

    class Meta:
        model = Product
        exclude = ()

        labels = LABELS['product']

        widgets = {
            'product_sap_id': forms.TextInput(attrs=SAP_STYLE),
            'index': forms.TextInput(attrs=BASIC_STYLE),
            'description': forms.TextInput(attrs=BASIC_REQ_STYLE)
        }

        error_messages = ERROR_MSG['product']


class SpecificationForm(forms.ModelForm):
    """Provide form for specification crud operations
    & hint messages for client side validation.
    """
    validation_hints = HINTS['specification']

    class Meta:
        model = Specification
        exclude = ('product', )

        labels = LABELS['specification']

        widgets = {
            'internal_diameter_target': forms.TextInput(attrs=NUM_STYLE),
            'internal_diameter_tolerance_top': forms.TextInput(attrs=NUM_STYLE),
            'internal_diameter_tolerance_bottom': forms.TextInput(attrs=NUM_STYLE),
            'external_diameter_target': forms.TextInput(attrs=NUM_STYLE),
            'external_diameter_tolerance_top': forms.TextInput(attrs=NUM_STYLE),
            'external_diameter_tolerance_bottom': forms.TextInput(attrs=NUM_STYLE),
            'wall_thickness_target': forms.TextInput(attrs=NUM_STYLE),
            'wall_thickness_tolerance_top': forms.TextInput(attrs=NUM_STYLE),
            'wall_thickness_tolerance_bottom': forms.TextInput(attrs=NUM_STYLE),
            'length_target': forms.TextInput(attrs=NUM_STYLE),
            'length_tolerance_top': forms.TextInput(attrs=NUM_STYLE),
            'length_tolerance_bottom': forms.TextInput(attrs=NUM_STYLE),
            'flat_crush_resistance_target': forms.TextInput(attrs=INT_STYLE),
            'flat_crush_resistance_tolerance_top': forms.TextInput(attrs=INT_STYLE),
            'flat_crush_resistance_tolerance_bottom': forms.TextInput(attrs=INT_STYLE),
            'moisture_content_target': forms.TextInput(attrs=INT_STYLE),
            'moisture_content_tolerance_top': forms.TextInput(attrs=INT_STYLE),
            'moisture_content_tolerance_bottom': forms.TextInput(attrs=INT_STYLE),
            'colour': forms.TextInput(attrs=BASIC_REQ_STYLE),
            'finish': forms.TextInput(attrs=BASIC_REQ_STYLE),
            'maximum_height_of_pallet': forms.TextInput(attrs=NUM_STYLE),
            'pallet_wrapped_with_stretch_film': forms.Select(attrs=BASIC_NO_HINTS_STYLE),
            'pallet_protected_with_paper_edges': forms.Select(attrs=BASIC_NO_HINTS_STYLE),
            'cores_packed_in': forms.Select(attrs=BASIC_NO_HINTS_STYLE),
            'quantity_on_the_pallet': forms.TextInput(attrs=INT_STYLE),
            'remarks': forms.Textarea(attrs={**BASIC_REQ_STYLE, **{'rows': 5, 'cols': 40}, })
        }


class ProductSpecificationMultiForm(MultiModelForm):
    """Wrap product & specification forms for product views simplicity."""
    form_classes = {
        'product': ProductForm,
        'spec': SpecificationForm,
    }


class SpecificationIssueForm(forms.Form):
    validation_hints = {'client_sap_id': HINTS['client']['client_sap_id'],
                        'date_of_issue': HINTS['order']['date_of_production'], }

    client_sap_id = forms.CharField(widget=forms.TextInput(attrs=SAP_STYLE), label='Numer SAP klienta')
    date_of_issue = forms.DateField(widget=DatePickerInput(options={'showClear': False, 'locale': 'pl', },
                                    attrs={**BASIC_STYLE, },
                                    format='%Y-%m-%d'), label='Data wystawienia specyfikacji')
