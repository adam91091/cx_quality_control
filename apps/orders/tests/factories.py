import factory
from abc import ABC, abstractmethod

from apps.clients.tests.factories import ClientFactory
from apps.constants import ORDER_SAP_DIGITS, FLOAT_DEFAULT, INT_DEFAULT
from apps.orders.models import Order, Measurement, MeasurementReport
from apps.products.tests.factories import ProductFactory


class OrderFactory(factory.DjangoModelFactory):
    class Meta:
        model = Order

    order_sap_id = factory.Sequence(lambda n: 10 ** (ORDER_SAP_DIGITS - 1) + n)
    client = factory.SubFactory(ClientFactory)
    product = factory.SubFactory(ProductFactory)
    date_of_production = '4098-12-12'
    status = 'Started'
    quantity = factory.Sequence(lambda n: n)
    # tube sizing information
    internal_diameter_reference = factory.Sequence(lambda n: FLOAT_DEFAULT + n)
    external_diameter_reference = factory.Sequence(lambda n: FLOAT_DEFAULT + n)
    length = factory.Sequence(lambda n: FLOAT_DEFAULT + n)


class MeasurementReportFactory(factory.DjangoModelFactory):
    class Meta:
        model = MeasurementReport

    order = factory.SubFactory(OrderFactory)
    author = factory.Sequence(lambda n: f"Author nr {n}")
    date_of_control = '4098-12-12'


class MeasurementFactory(factory.DjangoModelFactory):
    class Meta:
        model = Measurement

    measurement_report = factory.SubFactory(MeasurementReportFactory)
    pallet_number = factory.Sequence(lambda n: INT_DEFAULT + n)

    internal_diameter_tolerance_top = factory.Sequence(lambda n: FLOAT_DEFAULT + n)
    internal_diameter_target = factory.Sequence(lambda n: FLOAT_DEFAULT + n)
    internal_diameter_tolerance_bottom = factory.Sequence(lambda n: FLOAT_DEFAULT + n)

    external_diameter_tolerance_top = factory.Sequence(lambda n: FLOAT_DEFAULT + n)
    external_diameter_target = factory.Sequence(lambda n: FLOAT_DEFAULT + n)
    external_diameter_tolerance_bottom = factory.Sequence(lambda n: FLOAT_DEFAULT + n)

    length_tolerance_top = factory.Sequence(lambda n: FLOAT_DEFAULT + n)
    length_target = factory.Sequence(lambda n: FLOAT_DEFAULT + n)
    length_tolerance_bottom = factory.Sequence(lambda n: FLOAT_DEFAULT + n)

    flat_crush_resistance_target = factory.Sequence(lambda n: n)
    moisture_content_target = factory.Sequence(lambda n: n)
    weight = factory.Sequence(lambda n: n)

    remarks = factory.Sequence(lambda n: f'Remarks for object nr: {n}')


class PostDictProvider(ABC):

    @abstractmethod
    def get_post_data_as_dict(self):
        pass


class MeasurementReportPostDictProvider(PostDictProvider):
    def __init__(self):
        self.post_dict = factory.build(dict, FACTORY_CLASS=MeasurementReportFactory)

    def get_post_data_as_dict(self):
        for key in self.post_dict:
            if key == 'order':
                self.post_dict['order_sap_id'] = self.post_dict[key].order_sap_id
                del self.post_dict[key]
        return self.post_dict


class MeasurementsPostDictProvider(PostDictProvider):
    def __init__(self, measurements_count, start_from=0, initial_forms=0):
        self.post_dict = {
            'measurements-TOTAL_FORMS': measurements_count,
            'measurements-INITIAL_FORMS': initial_forms,
            'measurements-MIN_NUM_FORMS': 1,
            'measurements-MAX_NUM_FORMS': 100,
        }
        for i in range(start_from, measurements_count):
            meas_dict = factory.build(dict, FACTORY_CLASS=MeasurementFactory)
            for key in meas_dict:
                if key != 'measurement_report':
                    self.post_dict[f'measurements-{i}-{key}'] = meas_dict[key]
                if key == 'pallet_number':
                    self.post_dict[f'measurements-{i}-{key}'] = i

    def get_post_data_as_dict(self):
        return self.post_dict


class OrderPostDictProvider(PostDictProvider):
    def __init__(self):
        self.post_dict = factory.build(dict, FACTORY_CLASS=OrderFactory)

    def get_post_data_as_dict(self):
        for key in self.post_dict:
            if key == 'client':
                self.post_dict[key] = self.post_dict[key].client_sap_id
            elif key == 'product':
                self.post_dict[key] = self.post_dict[key].product_sap_id
        return self.post_dict
