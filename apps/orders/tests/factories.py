import factory

from apps.clients.tests.factories import ClientFactory
from apps.orders.models import Order, Measurement, MeasurementReport
from apps.products.tests.factories import ProductFactory


class OrderFactory(factory.DjangoModelFactory):
    class Meta:
        model = Order

    order_sap_id = factory.Sequence(lambda n: 100000 + n)
    client = factory.SubFactory(ClientFactory)
    product = factory.SubFactory(ProductFactory)
    date_of_production = '4098-12-12'
    status = 'Started'
    quantity = factory.Sequence(lambda n: n)
    # tube sizing information
    internal_diameter_reference = factory.Sequence(lambda n: 1.0 + n)
    external_diameter_reference = factory.Sequence(lambda n: 1.0 + n)
    length = factory.Sequence(lambda n: 1.0 + n)


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
    pallet_number = factory.Sequence(lambda n: 1 + n)

    internal_diameter_tolerance_top = factory.Sequence(lambda n: 1.0 + n)
    internal_diameter_target = factory.Sequence(lambda n: 1.0 + n)
    internal_diameter_tolerance_bottom = factory.Sequence(lambda n: 1.0 + n)

    external_diameter_tolerance_top = factory.Sequence(lambda n: 1.0 + n)
    external_diameter_target = factory.Sequence(lambda n: 1.0 + n)
    external_diameter_tolerance_bottom = factory.Sequence(lambda n: 1.0 + n)

    length_tolerance_top = factory.Sequence(lambda n: 1.0 + n)
    length_target = factory.Sequence(lambda n: 1.0 + n)
    length_tolerance_bottom = factory.Sequence(lambda n: 1.0 + n)

    flat_crush_resistance_target = factory.Sequence(lambda n: n)
    moisture_content_target = factory.Sequence(lambda n: n)
    weight = factory.Sequence(lambda n: n)

    remarks = factory.Sequence(lambda n: f'Remarks for object nr: {n}')
