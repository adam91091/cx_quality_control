from django.test import TestCase, Client as ViewClient

from apps.products.forms import ProductForm, SpecificationForm
from apps.products.models import Product, Specification
from apps.unittest_utils import assert_response_post, assert_response_get


class ProductsViewTest(TestCase):
    def setUp(self) -> None:
        self.view_client = ViewClient()
        self.number_of_products = 3
        for product_id in range(100000, 100000 + self.number_of_products):
            product = Product(product_sap_id=product_id, description="Product_description")
            spec = Specification(product=product)
            for field in spec._meta.get_fields():
                if field.name != 'product':
                    setattr(spec, field.name, 1)
            product.specification = spec
            product.save()
            spec.product = product
            spec.save()

        self.product_to_be_deleted = Product.objects.get(product_sap_id=100001)
        self.product_to_be_updated = Product.objects.get(product_sap_id=100002)

        self.data_to_post = {'product_sap_id': 123456, 'description': "Product new", 'index': ""}
        for field in Specification._meta.get_fields():
            if field.name != 'product':
                self.data_to_post[field.name] = '1'
        self.data_to_post['pallet_protected_with_paper_edges'] = 'Y'
        self.data_to_post['cores_packed_in'] = 'Horizontal'
        self.data_to_post['pallet_wrapped_with_stretch_film'] = 'Y'

    def test_list(self):
        response = assert_response_get(test_case=self, url_name='products:products_list',
                                       exp_status_code=200, exp_template='products_list.html')
        self.assertEqual(len(response.context['products']), self.number_of_products)

    def test_new_get(self):
        response = assert_response_get(test_case=self, url_name='products:product_new',
                                       exp_status_code=200, exp_template='product_form.html')
        self.assertTrue(isinstance(response.context['product_form'], ProductForm))
        self.assertTrue(isinstance(response.context['spec_form'], SpecificationForm))

    def test_new_post(self):
        product_sap_id = self.data_to_post['product_sap_id']
        assert_response_post(test_case=self, url_name='products:product_new',
                             exp_status_code=302, data=self.data_to_post)
        self.number_of_products += 1
        self.assertTrue(Product.objects.get(product_sap_id=product_sap_id))

    def test_delete_get(self):
        response = assert_response_get(test_case=self, url_name='products:product_delete', exp_status_code=200,
                                       exp_template='product_confirm_delete.html', id=self.product_to_be_deleted.id)
        self.assertEqual(response.context['product'].id, self.product_to_be_deleted.id)

    def test_delete_post(self):
        assert_response_post(test_case=self, url_name='products:product_delete', exp_status_code=302,
                             data={}, id=self.product_to_be_deleted.id)
        self.number_of_products -= 1
        self.assertFalse(Product.objects.filter(id=self.product_to_be_deleted.id))

    def test_update_get(self):
        response = assert_response_get(test_case=self, url_name='products:product_update', exp_status_code=200,
                                       exp_template='product_form.html', id=self.product_to_be_updated.id)
        self.assertEqual(response.context['product_form'].instance.id, self.product_to_be_updated.id)
        self.assertEqual(response.context['spec_form'].instance.product_id, self.product_to_be_updated.id)

    def test_update_post(self):
        updated_product_desc = 'Updated_description'
        self.data_to_post['description'] = updated_product_desc
        assert_response_post(test_case=self, url_name='products:product_update', exp_status_code=302,
                             data=self.data_to_post, id=self.product_to_be_updated.id)
        self.assertEqual(Product.objects.get(id=self.product_to_be_updated.id).description, updated_product_desc)
