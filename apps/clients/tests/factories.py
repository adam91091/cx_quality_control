import factory
from apps.clients.models import Client
from apps.globals import CLIENT_SAP_DIGITS


class ClientFactory(factory.DjangoModelFactory):
    class Meta:
        model = Client

    client_sap_id = factory.Sequence(lambda n: 10 ** (CLIENT_SAP_DIGITS - 1) + n)
    client_name = factory.Sequence(lambda n: f"test_client_{n}")
