from django.test import TestCase, Client as ViewClient

from apps.clients.tests.factories import ClientFactory
from apps.orders.forms import OrderForm
from apps.orders.models import Order
from apps.orders.tests.factories import OrderFactory
from apps.products.tests.factories import ProductFactory
from apps.unittest_utils import assert_response_post, assert_response_get


class OrdersViewTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.view_client = ViewClient()
        cls.clients = ClientFactory.create_batch(size=6)
        cls.products = ProductFactory.create_batch(size=6)
        cls.orders = [OrderFactory.create(product=product,
                                          client=client) for client, product in zip(cls.clients, cls.products)]
        cls.order_to_be_deleted = cls.orders[0]
        cls.order_to_be_updated = cls.orders[1]

        cls.client_sap_id_form_data = cls.clients[-1].client_sap_id
        cls.product_sap_id_form_data = cls.products[-1].product_sap_id
        cls.form_data = {'order_sap_id': 999999, 'client': cls.client_sap_id_form_data,
                         'product': cls.product_sap_id_form_data, 'date_of_production': '5896-12-12',
                         'status': 'Ready', 'quantity': 10, 'internal_diameter_reference': 1.7,
                         'external_diameter_reference': 1.2, 'length': 42.3}

    def test_list(self):
        response = assert_response_get(test_case=self, url_name='orders:orders_list',
                                       exp_status_code=200, exp_template='orders_list.html')
        self.assertEqual(len(response.context['orders']), len(self.orders))

    def test_new_get(self):
        response = assert_response_get(test_case=self, url_name='orders:order_new',
                                       exp_status_code=200, exp_template='order_form.html')
        self.assertTrue(isinstance(response.context['order_form'], OrderForm))

    def test_new_post(self):
        order_sap_id = self.form_data['order_sap_id']
        assert_response_post(test_case=self, url_name='orders:order_new',
                             exp_status_code=302, data=self.form_data)
        self.assertTrue(Order.objects.get(order_sap_id=order_sap_id))

    def test_delete_get(self):
        response = assert_response_get(test_case=self, url_name='orders:order_delete', exp_status_code=200,
                                       exp_template='order_confirm_delete.html', id=self.order_to_be_deleted.id)
        self.assertEqual(response.context['order'].id, self.order_to_be_deleted.id)

    def test_delete_post(self):
        assert_response_post(test_case=self, url_name='orders:order_delete', exp_status_code=302,
                             data={}, id=self.order_to_be_deleted.id)
        self.assertFalse(Order.objects.filter(id=self.order_to_be_deleted.id))

    def test_update_get(self):
        response = assert_response_get(test_case=self, url_name='orders:order_update', exp_status_code=200,
                                       exp_template='order_form.html', id=self.order_to_be_updated.id)
        self.assertEqual(response.context['order_form'].instance.id, self.order_to_be_updated.id)

    def test_update_post(self):
        updated_order_sap_id = 888888
        self.form_data['order_sap_id'] = updated_order_sap_id
        assert_response_post(test_case=self, url_name='orders:order_update', exp_status_code=302,
                             data=self.form_data, id=self.order_to_be_updated.id)
        self.assertEqual(Order.objects.get(id=self.order_to_be_updated.id).order_sap_id, updated_order_sap_id)
