import factory
from abc import ABC, abstractmethod

from apps.orders.tests.factories import MeasurementReportFactory, MeasurementFactory, OrderFactory


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
