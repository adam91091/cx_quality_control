import datetime

from django.test import TestCase

from apps.clients.tests.factories import ClientFactory
from apps.orders.models import Measurement
from apps.orders.tests.factories import OrderFactory, MeasurementReportFactory, MeasurementFactory
from apps.products.tests.factories import ProductFactory

from apps.orders.forms import OrderForm, MeasurementReportForm, MeasurementForm


class OrderFormTest(TestCase):
    def setUp(self) -> None:
        self.client = ClientFactory.create()
        self.product = ProductFactory.create()
        self.order = OrderFactory.create(product=self.product, client=self.client)

        self.form_data = {'order_sap_id': 999999, 'client': self.client.client_sap_id,
                          'product': self.product.product_sap_id, 'date_of_production': '5896-12-12',
                          'status': 'Ready', 'quantity': 10, 'internal_diameter_reference': 1.7,
                          'external_diameter_reference': 1.2, 'length': 42.3}

    def test_form_sap_id_validation_positive(self):
        self.form_data['order_sap_id'] = '765432'
        order_form = OrderForm(data=self.form_data, instance=self.order)
        self.assertTrue(order_form.is_valid())

    def test_form_sap_id_validation_negative(self):
        data = ['234', 'test', '14467']
        for value in data:
            self.form_data['order_sap_id'] = value
            order_form = OrderForm(data=self.form_data, instance=self.order)
            self.assertFalse(order_form.is_valid(), msg=f"Value: {value}")

    def test_form_numeric_field_validation_positive(self):
        data = ['1', '0.3', '12.323223', '.2']
        for value in data:
            self.form_data['internal_diameter_reference'] = value
            order_form = OrderForm(data=self.form_data, instance=self.order)
            self.assertTrue(order_form.is_valid(), msg=f"Value: {value}")

    def test_form_numeric_field_validation_negative(self):
        data = ['test', '-1']
        for value in data:
            self.form_data['external_diameter_reference'] = value
            order_form = OrderForm(data=self.form_data, instance=self.order)
            self.assertFalse(order_form.is_valid(), msg=f"Value: {value}")

    def test_form_integer_field_validation_positive(self):
        value = '42'
        self.form_data['quantity'] = value
        order_form = OrderForm(data=self.form_data, instance=self.order)
        self.assertTrue(order_form.is_valid(), msg=f"Value: {value}")

    def test_form_integer_field_validation_negative(self):
        data = ['test', '1.43', '4.test0']
        for value in data:
            self.form_data['quantity'] = value
            order_form = OrderForm(data=self.form_data, instance=self.order)
            self.assertFalse(order_form.is_valid(), msg=f"Value: {value}")

    def test_form_date_field_validation_positive(self):
        data = ['4897-12-04', datetime.date.today().strftime('%Y-%m-%d')]
        for value in data:
            self.form_data['date_of_production'] = value
            order_form = OrderForm(data=self.form_data, instance=self.order)
            self.assertTrue(order_form.is_valid(), msg=f"Value: {value}")


class MeasurementReportFormTest(TestCase):
    def setUp(self):
        self.client = ClientFactory.create()
        self.product = ProductFactory.create()
        self.order = OrderFactory.create(product=self.product, client=self.client)
        self.measurement_report = MeasurementReportFactory.create(order=self.order)
        self.form_data = {'date_of_control': '4892-09-05', 'author': 'Jan Kowalski'}

    def test_form_date_field_validation_positive(self):
        data = ['4597-12-04', datetime.date.today().strftime('%Y-%m-%d')]
        for value in data:
            self.form_data['date_of_production'] = value
            measurement_form = MeasurementReportForm(data=self.form_data, instance=self.measurement_report)
            self.assertTrue(measurement_form.is_valid(), msg=f"Value: {value}")


class MeasurementFormTest(TestCase):
    def setUp(self):
        self.client = ClientFactory.create()
        self.product = ProductFactory.create()
        self.order = OrderFactory.create(product=self.product, client=self.client)
        self.measurement_report = MeasurementReportFactory.create(order=self.order)
        self.measurement = MeasurementFactory.create(measurement_report=self.measurement_report)
        self.form_data = {}
        for field in Measurement._meta.get_fields():
            if field.name not in ['id', 'measurement_report']:
                self.form_data[field.name] = '1'

    def test_form_numeric_field_validation_positive(self):
        data = ['1', '0.3', '12.323223', '.2']
        for value in data:
            self.form_data['internal_diameter_target'] = value
            meas_form = MeasurementForm(data=self.form_data, instance=self.measurement)
            self.assertTrue(meas_form.is_valid(), msg=f"Value: {value}")

    def test_form_numeric_field_validation_negative(self):
        data = ['test', '-1']
        for value in data:
            self.form_data['external_diameter_tolerance_top'] = value
            meas_form = MeasurementForm(data=self.form_data, instance=self.measurement)
            self.assertFalse(meas_form.is_valid(), msg=f"Value: {value}")

    def test_form_integer_field_validation_positive(self):
        value = '42'
        self.form_data['pallet_number'] = value
        meas_form = MeasurementForm(data=self.form_data, instance=self.measurement)
        self.assertTrue(meas_form.is_valid(), msg=f"Value: {value}")

    def test_form_integer_field_validation_negative(self):
        data = ['test', '1.43', '4.test0']
        for value in data:
            self.form_data['pallet_number'] = value
            meas_form = MeasurementForm(data=self.form_data, instance=self.measurement)
            self.assertFalse(meas_form.is_valid(), msg=f"Value: {value}")
