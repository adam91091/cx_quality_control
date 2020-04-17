import factory
from apps.clients.models import Client


class ClientFactory(factory.DjangoModelFactory):
    class Meta:
        model = Client

    client_sap_id = factory.Sequence(lambda n: 100000 + n)
    client_name = factory.Sequence(lambda n: f"test_client_{n}")
