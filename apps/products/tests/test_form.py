from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.products.forms import ProductForm, SpecificationForm
from apps.products.models import Product, Specification


class ClientModelTest(TestCase):
    def setUp(self) -> None:
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

        self.product_form = ProductForm(instance=product)
        self.spec_form = SpecificationForm(instance=product.specification)

    def test_form_sap_id_validation_positive(self):
        self.product_form.product_sap_id = 765462
        self.product = self.product_form.save(commit=False)
        self.assertEqual(self.product.save(), None)

    def test_form_sap_id_validation_negative(self):
        data = [0, 234, 'test', 14467]
        for value in data:
            with self.assertRaises(AttributeError) as context:
                self.product_form.product_sap_id = value
                self.product_form.save()

    def test_form_numeric_field_validation_positive(self):
        data = [1, 0.3, 12.323223, 'test']
        for value in data:
            self.spec_form.internal_diameter_tolerance_bottom = value
            self.specification = self.spec_form.save(commit=False)
            self.assertEqual(self.specification.save(), None)

    def test_form_numeric_field_validation_negative(self):
        data = ['.1', 'test', '-1', .4]
        for value in data:
            with self.assertRaises(AttributeError) as context:
                self.spec_form.external_diameter_target = value
                self.spec_form.save()

    def test_form_integer_field_validation_negative(self):
        data = ['test', '1.43', '4.test0', '-9', 1]
        for value in data:
            with self.assertRaises(AttributeError) as context:
                self.spec_form.moisture_content_target = value
                self.spec_form.save()

    def test_form_integer_field_validation_positive(self):
        data = 42
        self.spec_form.moisture_content_target = data
        self.specification = self.spec_form.save(commit=False)
        self.assertEqual(self.specification.save(), None)
