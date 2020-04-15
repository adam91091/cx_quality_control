from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.products.forms import ProductForm, SpecificationForm
from apps.products.models import Product, Specification


class ClientModelTest(TestCase):
    def setUp(self) -> None:
        self.product_data = {'product_sap_id': 123456, 'description': "Product new", 'index': ""}
        self.spec_data = {}
        for field in Specification._meta.get_fields():
            if field.name != 'product':
                self.spec_data[field.name] = '1'
        self.spec_data['pallet_protected_with_paper_edges'] = 'Y'
        self.spec_data['cores_packed_in'] = 'Horizontal'
        self.spec_data['pallet_wrapped_with_stretch_film'] = 'Y'

        product_sap_id = 987654
        product = Product(product_sap_id=product_sap_id, description="Product_description")
        spec = Specification(product=product)
        for field in spec._meta.get_fields():
            if field.name != 'product':
                setattr(spec, field.name, 1)
            elif field.name in ['pallet_protected_with_paper_edges', 'pallet_wrapped_with_stretch_film']:
                setattr(spec, field.name, 'Y')
            elif field.name == 'cores_packed_in':
                setattr(spec, field.name, 'Horizontal')

        product.specification = spec
        product.save()
        spec.product = product
        spec.save()
        self.product = product
        self.spec = spec

    def test_form_sap_id_validation_positive(self):
        self.product_data['product_sap_id'] = '765432'
        product_form = ProductForm(data=self.product_data, instance=self.product)
        self.assertTrue(product_form.is_valid())

    def test_form_sap_id_validation_negative(self):
        data = ['234', 'test', '14467']
        for value in data:
            self.product_data['product_sap_id'] = value
            product_form = ProductForm(data=self.product_data, instance=self.product)
            self.assertFalse(product_form.is_valid())

    def test_form_numeric_field_validation_positive(self):
        data = ['1', '0.3', '12.323223', '.2']
        for value in data:
            self.spec_data['internal_diameter_tolerance_bottom'] = value
            spec_form = SpecificationForm(data=self.spec_data, instance=self.spec)
            self.assertTrue(spec_form.is_valid())

    def test_form_numeric_field_validation_negative(self):
        data = ['test', '-1']
        for value in data:
            self.spec_data['external_diameter_target'] = value
            spec_form = SpecificationForm(data=self.spec_data, instance=self.spec)
            self.assertFalse(spec_form.is_valid(), msg=f"Value: {value}")

    def test_form_integer_field_validation_positive(self):
        value = '42'
        self.spec_data['moisture_content_target'] = value
        spec_form = SpecificationForm(data=self.spec_data, instance=self.spec)
        self.assertTrue(spec_form.is_valid())

    def test_form_integer_field_validation_negative(self):
        data = ['test', '1.43', '4.test0']
        for value in data:
            self.spec_data['moisture_content_target'] = value
            spec_form = SpecificationForm(data=self.spec_data, instance=self.spec)
            self.assertFalse(spec_form.is_valid(), msg=f"Value: {value}")
