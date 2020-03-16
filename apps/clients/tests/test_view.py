from django.test import TestCase, Client as ViewClient
from django.urls import reverse

from apps.clients.forms import ClientForm
from apps.clients.models import Client


class ClientsViewTest(TestCase):
    def setUp(self) -> None:
        self.client = ViewClient()
        self.number_of_clients = 6
        for client_id in range(self.number_of_clients):
            Client.objects.create(client_sap_id=client_id,
                                  client_name=f"Client_with_id_{client_id}")
        self.client_to_be_deleted = Client.objects.get(client_sap_id=1)
        self.client_to_be_updated = Client.objects.get(client_sap_id=2)

    def test_list(self):
        response = self._assert_response_get(url_name='clients:clients_list', exp_status_code=200,
                                             exp_template='clients_list.html')
        self.assertEqual(len(response.context['clients']), self.number_of_clients)

    def test_new_get(self):
        response = self._assert_response_get(url_name='clients:client_new', exp_status_code=200,
                                             exp_template='client_form.html')
        self.assertTrue(isinstance(response.context['client_form'], ClientForm))

    def test_new_post(self):
        client_sap_id = 123456
        response = self.client.post(reverse('clients:client_new'), data={'client_sap_id': client_sap_id,
                                                                         'client_name': 'New with Post'})
        self.number_of_clients += 1
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Client.objects.get(client_sap_id=client_sap_id))

    def test_delete_get(self):
        response = self._assert_response_get(url_name='clients:client_delete', exp_status_code=200,
                                             exp_template='client_confirm_delete.html',
                                             id=self.client_to_be_deleted.id)
        self.assertEqual(response.context['client'].id, self.client_to_be_deleted.id)

    def test_delete_post(self):
        response = self.client.post(reverse('clients:client_delete', args=[self.client_to_be_deleted.id, ]))
        self.number_of_clients -= 1
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Client.objects.filter(id=self.client_to_be_deleted.id))

    def test_update_get(self):
        response = self._assert_response_get(url_name='clients:client_update', exp_status_code=200,
                                             exp_template='client_form.html', id=self.client_to_be_updated.id)
        self.assertEqual(response.context['client_form'].instance.id, self.client_to_be_updated.id)

    def test_update_post(self):
        updated_client_name = 'Updated_name'
        response = self.client.post(reverse('clients:client_update', args=[self.client_to_be_updated.id, ]),
                                    data={'client_sap_id': self.client_to_be_updated.client_sap_id,
                                          'client_name': updated_client_name})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Client.objects.get(id=self.client_to_be_updated.id).client_name, updated_client_name)

    def _assert_response_get(self, url_name, exp_status_code, exp_template, id=None):
        if id is not None:
            response = self.client.get(reverse(url_name, args=[id, ]))
        else:
            response = self.client.get(reverse(url_name))
        self.assertEqual(response.status_code, exp_status_code)
        self.assertTemplateUsed(response, exp_template)
        return response
