from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.clients.forms import ClientForm
from apps.clients.models import Client


class ClientModelTest(TestCase):
    def setUp(self) -> None:
        client_sap_id = 987654
        self.client = Client.objects.create(client_sap_id=client_sap_id,
                                            client_name=f"Client model with sap_id{client_sap_id}")
        self.client_form = ClientForm(instance=self.client)

    def test_form_sap_id_validation_positive(self):
        self.client_form.client_sap_id = 765463
        self.client = self.client_form.save(commit=False)
        self.client.save()

    def test_form_sap_id_validation_negative(self):
        data = [0, 234, 'test', 14467]
        for value in data:
            with self.assertRaises(AttributeError) as context:
                self.client_form.client_sap_id = value
                self.client_form.save()
