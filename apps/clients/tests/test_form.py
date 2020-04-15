from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.clients.forms import ClientForm
from apps.clients.models import Client


class ClientModelTest(TestCase):
    def setUp(self) -> None:
        self.data = {'client_sap_id': '987654', 'client_name': 'TestForm'}
        self.client = Client.objects.create(**self.data)

    def test_form_sap_id_validation_positive(self):
        self.data['client_sap_id'] = '765432'
        client_form = ClientForm(data=self.data, instance=self.client)
        self.assertTrue(client_form.is_valid())

    def test_form_sap_id_validation_negative(self):
        data = ['0', '234', 'test', '14467']
        for value in data:
            self.data['client_sap_id'] = value
            client_form = ClientForm(data=self.data, instance=self.client)
            self.assertFalse(client_form.is_valid())
