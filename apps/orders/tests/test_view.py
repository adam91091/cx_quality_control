from math import ceil

from django.test import TestCase, Client as ViewClient

from apps.clients.tests.factories import ClientFactory
from apps.factories_utils import MeasurementReportPostDictProvider, MeasurementsPostDictProvider, OrderPostDictProvider
from apps.orders.forms import OrderForm, MeasurementReportForm, MeasurementFormSet
from apps.orders.models import Order
from apps.orders.tests.factories import OrderFactory, MeasurementFactory, MeasurementReportFactory
from apps.products.tests.factories import ProductFactory
from apps.providers import PAGINATION_OBJ_COUNT_PER_PAGE
from apps.unittest_utils import assert_response_post, assert_response_get
from apps.users.tests import PASSWORD
from apps.users.tests.factories import CxUserFactory


class OrdersViewTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        # Orders
        cls.view_client = ViewClient()
        cls.clients = ClientFactory.create_batch(size=6)
        cls.products = ProductFactory.create_batch(size=6)
        cls.orders = [OrderFactory.create(product=product,
                                          client=client) for client, product in zip(cls.clients, cls.products)]
        cls.order_to_be_deleted = cls.orders[0]
        cls.order_to_be_updated = cls.orders[1]

        cls.client_sap_id_form_data = cls.clients[-1].client_sap_id
        cls.product_sap_id_form_data = cls.products[-1].product_sap_id
        cls.form_data = {'order_sap_id': 99996599, 'client': cls.client_sap_id_form_data,
                         'product': cls.product_sap_id_form_data, 'date_of_production': '5896-12-12',
                         'status': 'Ready', 'quantity': 10, 'internal_diameter_reference': 1.7,
                         'external_diameter_reference': 1.2, 'length': 42.3}

        cls.user = CxUserFactory.create()

    def test_list(self):
        self.view_client.login(username=self.user.username, password=PASSWORD)
        response = assert_response_get(test_case=self, url_name='orders:orders_list',
                                       exp_status_code=200, exp_template='orders_list.html')
        self.assertEqual(response.context['page_obj'].paginator.num_pages,
                         ceil(len(self.orders) / PAGINATION_OBJ_COUNT_PER_PAGE))

    def test_new_get(self):
        self.view_client.login(username=self.user.username, password=PASSWORD)
        response = assert_response_get(test_case=self, url_name='orders:order-new',
                                       exp_status_code=200, exp_template='order_form.html')
        self.assertTrue(isinstance(response.context['form'], OrderForm))

    def test_new_post(self):
        self.view_client.login(username=self.user.username, password=PASSWORD)
        order_sap_id = self.form_data['order_sap_id']
        assert_response_post(test_case=self, url_name='orders:order-new',
                             exp_status_code=302, data=self.form_data)
        self.assertTrue(Order.objects.get(order_sap_id=order_sap_id))

    def test_delete_get(self):
        self.view_client.login(username=self.user.username, password=PASSWORD)
        response = assert_response_get(test_case=self, url_name='orders:order-delete', exp_status_code=200,
                                       exp_template='order_confirm_delete.html', id=self.order_to_be_deleted.id)
        self.assertEqual(response.context['order'].id, self.order_to_be_deleted.id)

    def test_delete_post(self):
        self.view_client.login(username=self.user.username, password=PASSWORD)
        assert_response_post(test_case=self, url_name='orders:order-delete', exp_status_code=302,
                             data={}, id=self.order_to_be_deleted.id)
        self.assertFalse(Order.objects.filter(id=self.order_to_be_deleted.id))

    def test_update_get(self):
        self.view_client.login(username=self.user.username, password=PASSWORD)
        response = assert_response_get(test_case=self, url_name='orders:order-update', exp_status_code=200,
                                       exp_template='order_form.html', id=self.order_to_be_updated.id)
        self.assertEqual(response.context['form'].instance.id, self.order_to_be_updated.id)

    def test_update_post(self):
        self.view_client.login(username=self.user.username, password=PASSWORD)
        updated_length = self.form_data['length']
        assert_response_post(test_case=self, url_name='orders:order-update', exp_status_code=302,
                             data=self.form_data, id=self.order_to_be_updated.id)
        self.assertEqual(Order.objects.get(id=self.order_to_be_updated.id).length, updated_length)


class MeasurementReportsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        # test variables
        cls.measurement_report_count = 6
        # new
        cls.view_client = ViewClient()
        cls.client = ClientFactory.create()
        cls.product = ProductFactory.create()
        cls.order_new = OrderFactory.create(client=cls.client, product=cls.product)

        # update
        cls.order_update = OrderFactory.create(client=cls.client, product=cls.product)
        cls.measurement_report = MeasurementReportFactory.create(order=cls.order_update)
        for i in range(cls.measurement_report_count):
            MeasurementFactory.create(measurement_report=cls.measurement_report)

        # post data
        cls.order_data = OrderPostDictProvider().get_post_data_as_dict()
        cls.meas_report_data = MeasurementReportPostDictProvider().get_post_data_as_dict()
        cls.meas_data = MeasurementsPostDictProvider(measurements_count=cls.measurement_report_count
                                                     ).get_post_data_as_dict()

        cls.form_data = {**cls.meas_data, **cls.meas_report_data, **{'client': cls.client.client_sap_id,
                                                                     'product': cls.product.product_sap_id,
                                                                     'date_of_production': '5896-12-12'}}

        cls.user = CxUserFactory.create()

    def test_new_get(self):
        self.view_client.login(username=self.user.username, password=PASSWORD)
        response = assert_response_get(test_case=self, url_name='orders:measurement_report_new', id=self.order_new.id,
                                       exp_status_code=200, exp_template='measurement_report_form.html')
        self.assertEqual(response.context['order_form'].instance, self.order_new)
        self.assertEqual(response.context['order_id'], self.order_new.id)

        self.assertTrue(isinstance(response.context['measurement_report_form'], MeasurementReportForm))
        self.assertTrue(isinstance(response.context['measurement_formset'], MeasurementFormSet))

    def test_new_post(self):
        self.view_client.login(username=self.user.username, password=PASSWORD)
        assert_response_post(test_case=self, url_name='orders:measurement_report_new', id=self.order_new.id,
                             exp_status_code=302, data=self.form_data)
        order_sap_id = self.form_data['order_sap_id']
        order = Order.objects.get(order_sap_id=order_sap_id)
        self.assertEqual(order.measurement_report.measurements.count(), self.measurement_report_count)

    def test_update_get(self):
        self.view_client.login(username=self.user.username, password=PASSWORD)
        response = assert_response_get(test_case=self, url_name='orders:measurement_report_update',
                                       id=self.order_update.id,
                                       exp_status_code=200, exp_template='measurement_report_form.html')
        self.assertEqual(response.context['order_form'].instance, self.order_update)
        self.assertEqual(response.context['order_id'], self.order_update.id)
        self.assertEqual(response.context['measurement_report_form'].instance, self.order_update.measurement_report)
        self.assertEqual(len(response.context['measurement_formset']), self.measurement_report_count)

    def test_update_post(self):
        self.view_client.login(username=self.user.username, password=PASSWORD)
        updated_measurements_count = 10
        add_meas_data = MeasurementsPostDictProvider(measurements_count=10, initial_forms=6,
                                                     start_from=6).get_post_data_as_dict()

        for i in range(self.measurement_report_count):
            self.form_data[f'measurements-{i}-id'] = self.order_update.measurement_report.measurements.all()[i].id
            self.form_data[f'measurements-{i}-measurement_report'] = self.order_update.measurement_report.id
        self.form_data.update(add_meas_data)
        assert_response_post(test_case=self, url_name='orders:measurement_report_update', exp_status_code=302,
                             data=self.form_data, id=self.order_update.id)
        updated_order = Order.objects.get(id=self.order_update.id)
        self.assertEqual(updated_order.measurement_report, self.order_update.measurement_report)
        self.assertEqual(updated_order.measurement_report.measurements.count(),
                         updated_measurements_count)
