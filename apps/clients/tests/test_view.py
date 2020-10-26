from math import ceil

from django.test import TestCase, Client as ViewClient

from .factories import ClientFactory

from apps.clients.forms import ClientForm
from apps.clients.models import Client
from apps.unittest_utils import assert_response_get, assert_response_post
from apps.providers import PAGINATION_OBJ_COUNT_PER_PAGE


class ClientsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.view_client = ViewClient()
        cls.clients = ClientFactory.create_batch(size=36)
        cls.client_to_be_deleted = cls.clients[0]
        cls.client_to_be_updated = cls.clients[1]

    def test_list(self):
        response = assert_response_get(test_case=self, url_name='clients:clients_list', exp_status_code=200,
                                       exp_template='clients_list.html')
        self.assertEqual(response.context['page_obj'].paginator.num_pages,
                         ceil(len(self.clients) / PAGINATION_OBJ_COUNT_PER_PAGE))

    def test_new_get(self):
        response = assert_response_get(test_case=self, url_name='clients:client_new', exp_status_code=200,
                                       exp_template='client_form.html')
        self.assertTrue(isinstance(response.context['client_form'], ClientForm))

    def test_new_post(self):
        client_sap_id = 1234565
        assert_response_post(test_case=self, url_name='clients:client_new', exp_status_code=302,
                             data={'client_sap_id': client_sap_id, 'client_name': 'New with Post'})
        self.assertTrue(Client.objects.get(client_sap_id=client_sap_id))

    def test_delete_get(self):
        response = assert_response_get(test_case=self, url_name='clients:client_delete', exp_status_code=200,
                                       exp_template='client_confirm_delete.html', id=self.client_to_be_deleted.id)
        self.assertEqual(response.context['client'].id, self.client_to_be_deleted.id)

    def test_delete_post(self):
        assert_response_post(test_case=self, url_name='clients:client_delete', exp_status_code=302,
                             data={}, id=self.client_to_be_deleted.id)
        self.assertFalse(Client.objects.filter(id=self.client_to_be_deleted.id))

    def test_update_get(self):
        response = assert_response_get(test_case=self, url_name='clients:client_update', exp_status_code=200,
                                       exp_template='client_form.html', id=self.client_to_be_updated.id)
        self.assertEqual(response.context['client_form'].instance.id, self.client_to_be_updated.id)

    def test_update_post(self):
        updated_client_name = 'Updated_name'
        assert_response_post(test_case=self, url_name='clients:client_update', exp_status_code=302,
                             data={'client_sap_id': self.client_to_be_updated.client_sap_id,
                                   'client_name': updated_client_name}, id=self.client_to_be_updated.id)
        self.assertEqual(Client.objects.get(id=self.client_to_be_updated.id).client_name, updated_client_name)
