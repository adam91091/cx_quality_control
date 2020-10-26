import factory

from apps.clients.tests.factories import ClientFactory
from apps.globals import ORDER_SAP_DIGITS, FLOAT_DEFAULT, INT_DEFAULT
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
