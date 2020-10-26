from django.test import TestCase

from apps.products.forms import ProductForm, SpecificationForm
from apps.products.models import Specification
from apps.products.tests.factories import ProductFactory, SpecificationFactory


class ProductFormTest(TestCase):
    def setUp(self) -> None:
        self.product = ProductFactory.create()
        self.spec = SpecificationFactory.create(product=self.product)

        self.product_form = {'product_sap_id': '1234563', 'description': "Product new", 'index': ""}
        self.spec_form = {}
        for field in Specification._meta.get_fields():
            if field.name != 'product':
                self.spec_form[field.name] = '1'
        self.spec_form['pallet_protected_with_paper_edges'] = 'Y'
        self.spec_form['cores_packed_in'] = 'Horizontal'
        self.spec_form['pallet_wrapped_with_stretch_film'] = 'Y'

    def test_form_sap_id_validation_positive(self):
        self.product_form['product_sap_id'] = '7654332'
        product_form = ProductForm(data=self.product_form, instance=self.product)
        self.assertTrue(product_form.is_valid())

    def test_form_sap_id_validation_negative(self):
        data = ['234', 'test', '14467']
        for value in data:
            self.product_form['product_sap_id'] = value
            product_form = ProductForm(data=self.product_form, instance=self.product)
            self.assertFalse(product_form.is_valid(), msg=f"Value: {value}")

    def test_form_numeric_field_validation_positive(self):
        data = ['1', '0.3', '12.323223', '.2']
        for value in data:
            self.spec_form['internal_diameter_tolerance_top'] = value
            spec_form = SpecificationForm(data=self.spec_form, instance=self.spec)
            self.assertTrue(spec_form.is_valid(), msg=f"Value: {value}")

    def test_form_numeric_field_validation_negative(self):
        data = ['test', '-1']
        for value in data:
            self.spec_form['external_diameter_target'] = value
            spec_form = SpecificationForm(data=self.spec_form, instance=self.spec)
            self.assertFalse(spec_form.is_valid(), msg=f"Value: {value}")

    def test_form_integer_field_validation_positive(self):
        value = '42'
        self.spec_form['moisture_content_target'] = value
        spec_form = SpecificationForm(data=self.spec_form, instance=self.spec)
        self.assertTrue(spec_form.is_valid(), msg=f"Value: {value}")

    def test_form_integer_field_validation_negative(self):
        data = ['test', '1.43', '4.test0']
        for value in data:
            self.spec_form['moisture_content_target'] = value
            spec_form = SpecificationForm(data=self.spec_form, instance=self.spec)
            self.assertFalse(spec_form.is_valid(), msg=f"Value: {value}")
