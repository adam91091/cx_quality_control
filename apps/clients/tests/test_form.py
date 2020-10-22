from django.test import TestCase

from .factories import ClientFactory
from apps.clients.forms import ClientForm


class ClientFormTest(TestCase):
    def setUp(self) -> None:
        self.client = ClientFactory()
        self.valid_client_form_data = {'client_sap_id': '7654322', 'client_name': 'test_client'}
        self.invalid_client_sap_ids = ['0', '234', 'test', '14467']

    def test_form_sap_id_validation_positive(self):
        client_form = ClientForm(data=self.valid_client_form_data, instance=self.client)
        self.assertTrue(client_form.is_valid(), msg=f"Value: {self.valid_client_form_data['client_sap_id']}")

    def test_form_sap_id_validation_negative(self):
        for value in self.invalid_client_sap_ids:
            self.valid_client_form_data['client_sap_id'] = value
            client_form = ClientForm(data=self.valid_client_form_data, instance=self.client)
            self.assertFalse(client_form.is_valid(), msg=f"Value: {value}")
