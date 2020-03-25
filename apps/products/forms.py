from django import forms
from django.forms import ModelForm

from apps.products.models import Product, Specification
from apps.validators import REGEXPS


class ProductForm(ModelForm):
    validation_hints = {'product_sap_id': "Numer SAP musi się składać z 6 cyfr oraz nie może być polem pustym",
                        'description': "Pole z opisem nie może być puste"}

    def __init__(self, read_only=False, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        if read_only:
            for field in self.fields.values():
                field.widget.attrs['readonly'] = True
                field.widget.attrs['disabled'] = 'true'

    class Meta:
        model = Product
        exclude = ()
        labels = {
            'product_sap_id': "Numer SAP produktu",
            'index': "Indeks produktu",
            'description': "Opis produktu",
        }
        widgets = {
            'product_sap_id': forms.TextInput(attrs={'class': 'form-control',
                                                     'pattern': REGEXPS['client']['client_sap_id'],
                                                     'required': 'true'}),
            'index': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control',
                                                  'required': 'true'})
        }
        error_messages = {
            'product_sap_id': {'unique': "Produkt o podanym numerze SAP już istnieje.",
                               }
        }


class SpecificationForm(ModelForm):
    validation_hints = {}

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
            'internal_diameter_target': forms.TextInput(attrs={'class': 'form-control',
                                                               'required': 'true'}),
            'internal_diameter_tolerance_top': forms.TextInput(attrs={'class': 'form-control',
                                                               'required': 'true'}),
            'internal_diameter_tolerance_bottom': forms.TextInput(attrs={'class': 'form-control',
                                                                      'required': 'true'}),
            'external_diameter_target': forms.TextInput(attrs={'class': 'form-control',
                                                                      'required': 'true'}),
            'external_diameter_tolerance_top': forms.TextInput(attrs={'class': 'form-control',
                                                                      'required': 'true'}),
            'external_diameter_tolerance_bottom': forms.TextInput(attrs={'class': 'form-control',
                                                                         'required': 'true'}),
            'wall_thickness_target': forms.TextInput(attrs={'class': 'form-control',
                                                               'required': 'true'}),
            'wall_thickness_tolerance_top': forms.TextInput(attrs={'class': 'form-control',
                                                                      'required': 'true'}),
            'wall_thickness_tolerance_bottom': forms.TextInput(attrs={'class': 'form-control',
                                                                         'required': 'true'}),
            'length_target': forms.TextInput(attrs={'class': 'form-control',
                                                            'required': 'true'}),
            'length_tolerance_top': forms.TextInput(attrs={'class': 'form-control',
                                                                   'required': 'true'}),
            'length_tolerance_bottom': forms.TextInput(attrs={'class': 'form-control',
                                                                      'required': 'true'}),
            'flat_crush_resistance_target': forms.TextInput(attrs={'class': 'form-control',
                                                            'required': 'true'}),
            'flat_crush_resistance_tolerance_top': forms.TextInput(attrs={'class': 'form-control',
                                                                   'required': 'true'}),
            'flat_crush_resistance_tolerance_bottom': forms.TextInput(attrs={'class': 'form-control',
                                                                      'required': 'true'}),
            'moisture_content_target': forms.TextInput(attrs={'class': 'form-control',
                                                                   'required': 'true'}),
            'moisture_content_tolerance_top': forms.TextInput(attrs={'class': 'form-control',
                                                                          'required': 'true'}),
            'moisture_content_tolerance_bottom': forms.TextInput(attrs={'class': 'form-control',
                                                                             'required': 'true'}),
            'colour': forms.TextInput(attrs={'class': 'form-control',
                                                                             'required': 'true'}),
            'finish': forms.TextInput(attrs={'class': 'form-control',
                                             'required': 'true'}),
            'maximum_height_of_pallet': forms.TextInput(attrs={'class': 'form-control',
                                             'required': 'true'}),
            'pallet_wrapped_with_stretch_film': forms.Select(attrs={'class': 'form-control'}),
            'pallet_protected_with_paper_edges': forms.Select(attrs={'class': 'form-control'}),
            'cores_packed_in': forms.Select(attrs={'class': 'form-control'}),
            'quantity_on_the_pallet': forms.TextInput(attrs={'class': 'form-control',
                                                                             'required': 'true'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 40,
                                                                             'required': 'true'})
        }
