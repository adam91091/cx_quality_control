from math import ceil

from django.test import TestCase, Client as ViewClient

from .factories import ClientFactory

from apps.clients.forms import ClientForm
from apps.clients.models import Client
from apps.unittest_helpers import assert_response_get, assert_response_post
from apps.constants import PAGINATION_OBJ_COUNT_PER_PAGE
from ...users.tests import PASSWORD
from ...users.tests.factories import CxUserFactory


class ClientsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.view_client = ViewClient()
        cls.clients = ClientFactory.create_batch(size=36)
        cls.client_to_be_deleted = cls.clients[0]
        cls.client_to_be_updated = cls.clients[1]
        cls.user = CxUserFactory.create()

    def test_list(self):
        self.view_client.login(username=self.user.username, password=PASSWORD)
        response = assert_response_get(test_case=self, url_name='clients:clients-list', exp_status_code=200,
                                       exp_template='clients_list.html')
        self.assertEqual(response.context['page_obj'].paginator.num_pages,
                         ceil(len(self.clients) / PAGINATION_OBJ_COUNT_PER_PAGE))

    def test_new_get(self):
        self.view_client.login(username=self.user.username, password=PASSWORD)
        response = assert_response_get(test_case=self, url_name='clients:client-new', exp_status_code=200,
                                       exp_template='client_form.html')
        self.assertTrue(isinstance(response.context['form'], ClientForm))

    def test_new_post(self):
        self.view_client.login(username=self.user.username, password=PASSWORD)
        client_sap_id = 1234565
        assert_response_post(test_case=self, url_name='clients:client-new', exp_status_code=302,
                             data={'client_sap_id': client_sap_id, 'client_name': 'New with Post'})
        self.assertTrue(Client.objects.get(client_sap_id=client_sap_id))

    def test_delete_get(self):
        self.view_client.login(username=self.user.username, password=PASSWORD)
        response = assert_response_get(test_case=self, url_name='clients:client-delete', exp_status_code=200,
                                       exp_template='client_confirm_delete.html', id=self.client_to_be_deleted.id)
        self.assertEqual(response.context['client'].id, self.client_to_be_deleted.id)

    def test_delete_post(self):
        self.view_client.login(username=self.user.username, password=PASSWORD)
        assert_response_post(test_case=self, url_name='clients:client-delete', exp_status_code=302,
                             data={}, id=self.client_to_be_deleted.id)
        self.assertFalse(Client.objects.filter(id=self.client_to_be_deleted.id))

    def test_update_get(self):
        self.view_client.login(username=self.user.username, password=PASSWORD)
        response = assert_response_get(test_case=self, url_name='clients:client-update', exp_status_code=200,
                                       exp_template='client_form.html', id=self.client_to_be_updated.id)
        self.assertEqual(response.context['form'].instance.id, self.client_to_be_updated.id)

    def test_update_post(self):
        self.view_client.login(username=self.user.username, password=PASSWORD)
        updated_client_name = 'Updated_name'
        assert_response_post(test_case=self, url_name='clients:client-update', exp_status_code=302,
                             data={'client_sap_id': self.client_to_be_updated.client_sap_id,
                                   'client_name': updated_client_name}, id=self.client_to_be_updated.id)
        self.assertEqual(Client.objects.get(id=self.client_to_be_updated.id).client_name, updated_client_name)
