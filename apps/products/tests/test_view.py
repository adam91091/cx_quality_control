from django.test import TestCase, Client as ViewClient

from apps.products.forms import ProductForm, SpecificationForm
from apps.products.models import Product, Specification
from apps.products.tests.factories import ProductFactory, SpecificationFactory
from apps.unittest_utils import assert_response_post, assert_response_get


class ProductsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.view_client = ViewClient()
        cls.products = ProductFactory.create_batch(size=6)
        cls.specifications = [SpecificationFactory.create(product=product) for product in cls.products]
        cls.product_to_be_deleted = cls.products[0]
        cls.product_to_be_updated = cls.products[1]

        cls.form_data = {'product_sap_id': 999999, 'description': "product_form_data", 'index': ""}
        for field in Specification._meta.get_fields():
            if field.name != 'product':
                cls.form_data[field.name] = '999'
        cls.form_data['pallet_protected_with_paper_edges'] = 'Y'
        cls.form_data['cores_packed_in'] = 'Horizontal'
        cls.form_data['pallet_wrapped_with_stretch_film'] = 'Y'

    def test_list(self):
        response = assert_response_get(test_case=self, url_name='products:products_list',
                                       exp_status_code=200, exp_template='products_list.html')
        self.assertEqual(len(response.context['products']), len(self.products))

    def test_new_get(self):
        response = assert_response_get(test_case=self, url_name='products:product_new',
                                       exp_status_code=200, exp_template='product_form.html')
        self.assertTrue(isinstance(response.context['product_form'], ProductForm))
        self.assertTrue(isinstance(response.context['spec_form'], SpecificationForm))

    def test_new_post(self):
        product_sap_id = self.form_data['product_sap_id']
        assert_response_post(test_case=self, url_name='products:product_new',
                             exp_status_code=302, data=self.form_data)
        self.assertTrue(Product.objects.get(product_sap_id=product_sap_id))

    def test_delete_get(self):
        response = assert_response_get(test_case=self, url_name='products:product_delete', exp_status_code=200,
                                       exp_template='product_confirm_delete.html', id=self.product_to_be_deleted.id)
        self.assertEqual(response.context['product'].id, self.product_to_be_deleted.id)

    def test_delete_post(self):
        assert_response_post(test_case=self, url_name='products:product_delete', exp_status_code=302,
                             data={}, id=self.product_to_be_deleted.id)
        self.assertFalse(Product.objects.filter(id=self.product_to_be_deleted.id))

    def test_update_get(self):
        response = assert_response_get(test_case=self, url_name='products:product_update', exp_status_code=200,
                                       exp_template='product_form.html', id=self.product_to_be_updated.id)
        self.assertEqual(response.context['product_form'].instance.id, self.product_to_be_updated.id)
        self.assertEqual(response.context['spec_form'].instance.product_id, self.product_to_be_updated.id)

    def test_update_post(self):
        updated_product_desc = 'Updated_description'
        self.form_data['description'] = updated_product_desc
        assert_response_post(test_case=self, url_name='products:product_update', exp_status_code=302,
                             data=self.form_data, id=self.product_to_be_updated.id)
        self.assertEqual(Product.objects.get(id=self.product_to_be_updated.id).description, updated_product_desc)
