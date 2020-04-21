import factory

from apps.clients.tests.factories import ClientFactory
from apps.orders.models import Order
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
