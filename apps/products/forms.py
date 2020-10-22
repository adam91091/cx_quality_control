from django import forms
from django.forms import ModelForm

from apps.forms_utils import NUM_STYLE, INT_STYLE, BASIC_REQ_STYLE, BASIC_STYLE, BASIC_NO_HINTS_STYLE, SAP_STYLE
from apps.products.models import Product, Specification


class ProductForm(ModelForm):
    validation_hints = {'product_sap_id': "Numer SAP musi się składać z 6 cyfr oraz nie może być polem pustym",
                        'description': "Pole z opisem nie może być puste", }

    def __init__(self, read_only=False, update=False, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        if read_only:
            for field in self.fields.values():
                field.widget.attrs['readonly'] = True
                field.widget.attrs['disabled'] = 'true'
        if update:
            self.fields['product_sap_id'].disabled = True

    class Meta:
        model = Product
        exclude = ()
        labels = {
            'product_sap_id': "Numer SAP produktu",
            'index': "Indeks produktu",
            'description': "Opis produktu",
        }
        widgets = {
            'product_sap_id': forms.TextInput(attrs=SAP_STYLE),
            'index': forms.TextInput(attrs=BASIC_STYLE),
            'description': forms.TextInput(attrs=BASIC_REQ_STYLE)
        }
        error_messages = {
            'product_sap_id': {'unique': "Produkt o podanym numerze SAP już istnieje.", }
        }


class SpecificationForm(ModelForm):
    validation_hints = {'remarks': "Pole z uwagami nie może być puste"}

    def __init__(self, read_only=False, *args, **kwargs):
        super(SpecificationForm, self).__init__(*args, **kwargs)
        if read_only:
            for field in self.fields.values():
                field.widget.attrs['readonly'] = True
                field.widget.attrs['disabled'] = 'true'

    class Meta:
        model = Specification
        exclude = ('product',)
        labels = {
            'internal_diameter_target': "Średnica wewnętrzna",
            'external_diameter_target': "Średnica zewnętrzna",
            'wall_thickness_target': "Grubość ścianki",
            'length_target': "Długość",
            'flat_crush_resistance_target': "Wytrzymałość na ściskanie (100 MM)",
            'moisture_content_target': "Wilgotność",
            'colour': "Kolor",
            'finish': "Powierzchnia zew.",
            'maximum_height_of_pallet': "Maksymalna wysokość palety",
            'pallet_wrapped_with_stretch_film': "Paleta zabezpieczona folią stretch?",
            'pallet_protected_with_paper_edges': "Paleta zabezpieczona kątownikami papierowymi?",
            'cores_packed_in': "Tuleje pakowane:",
            'quantity_on_the_pallet': "Ilość sztuk na palecie:",
            'remarks': "Uwagi",
        }
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
