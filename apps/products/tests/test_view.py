from math import ceil

from django.test import TestCase, Client as ViewClient

from apps.products.forms import ProductSpecificationMultiForm
from apps.products.models import Product, Specification
from apps.products.tests.factories import ProductFactory, SpecificationFactory
from apps.providers import PAGINATION_OBJ_COUNT_PER_PAGE
from apps.unittest_utils import assert_response_post, assert_response_get
from apps.users.tests import PASSWORD
from apps.users.tests.factories import CxUserFactory


class ProductsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.view_client = ViewClient()
        cls.products = ProductFactory.create_batch(size=6)
        cls.specifications = [SpecificationFactory.create(product=product) for product in cls.products]
        cls.product_to_be_deleted = cls.products[0]
        cls.product_to_be_updated = cls.products[1]

        cls.form_data = {'product-product_sap_id': 9993999,
                         'product-description': "product-product_form_data", 'product-index': ""}
        for field in Specification._meta.get_fields():
            if field.name != 'product':
                cls.form_data[f'spec-{field.name}'] = '999'
        cls.form_data['spec-pallet_protected_with_paper_edges'] = 'Y'
        cls.form_data['spec-cores_packed_in'] = 'Horizontal'
        cls.form_data['spec-pallet_wrapped_with_stretch_film'] = 'Y'

        cls.user = CxUserFactory.create()

    def test_list(self):
        self.view_client.login(username=self.user.username, password=PASSWORD)
        response = assert_response_get(test_case=self, url_name='products:products-list',
                                       exp_status_code=200, exp_template='products_list.html')
        self.assertEqual(response.context['page_obj'].paginator.num_pages,
                         ceil(len(self.products) / PAGINATION_OBJ_COUNT_PER_PAGE))

    def test_new_get(self):
        self.view_client.login(username=self.user.username, password=PASSWORD)
        response = assert_response_get(test_case=self, url_name='products:product-new',
                                       exp_status_code=200, exp_template='product_form.html')
        self.assertTrue(isinstance(response.context['form'], ProductSpecificationMultiForm))

    def test_new_post(self):
        self.view_client.login(username=self.user.username, password=PASSWORD)
        product_sap_id = self.form_data['product-product_sap_id']
        assert_response_post(test_case=self, url_name='products:product-new',
                             exp_status_code=302, data=self.form_data)
        self.assertTrue(Product.objects.get(product_sap_id=product_sap_id))

    def test_delete_get(self):
        self.view_client.login(username=self.user.username, password=PASSWORD)
        response = assert_response_get(test_case=self, url_name='products:product-delete', exp_status_code=200,
                                       exp_template='product_confirm_delete.html', id=self.product_to_be_deleted.id)
        self.assertEqual(response.context['product'].id, self.product_to_be_deleted.id)

    def test_delete_post(self):
        self.view_client.login(username=self.user.username, password=PASSWORD)
        assert_response_post(test_case=self, url_name='products:product-delete', exp_status_code=302,
                             data={}, id=self.product_to_be_deleted.id)
        self.assertFalse(Product.objects.filter(id=self.product_to_be_deleted.id))

    def test_update_get(self):
        self.view_client.login(username=self.user.username, password=PASSWORD)
        response = assert_response_get(test_case=self, url_name='products:product-update', exp_status_code=200,
                                       exp_template='product_form.html', id=self.product_to_be_updated.id)
        self.assertEqual(response.context['form']['product'].instance.id, self.product_to_be_updated.id)
        self.assertEqual(response.context['form']['spec'].instance.product_id, self.product_to_be_updated.id)

    def test_update_post(self):
        self.view_client.login(username=self.user.username, password=PASSWORD)
        updated_product_desc = 'Updated_description'
        self.form_data['product-description'] = updated_product_desc
        assert_response_post(test_case=self, url_name='products:product-update', exp_status_code=302,
                             data=self.form_data, id=self.product_to_be_updated.id)
        self.assertEqual(Product.objects.get(id=self.product_to_be_updated.id).description, updated_product_desc)
