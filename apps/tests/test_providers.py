from django.test import TestCase, Client as ViewClient

from apps.clients.models import Client
from apps.clients.tests.factories import ClientFactory
from apps.providers import ListViewFilterProvider, PAGINATION_OBJ_COUNT_PER_PAGE


class ListViewFilterProviderTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.view_client = ViewClient()
        response = cls.view_client.get('/mock/')
        cls.request = response.wsgi_request

    def test_pagination_basic(self):
        for obj_num, num_pages in [(31, 4), (7, 1)]:
            ClientFactory.create_batch(size=obj_num)
            provider = ListViewFilterProvider(request=self.request, model=Client)
            provider.paginate()
            self.assertEqual(provider.page_obj.paginator.num_pages, num_pages)
            Client.objects.all().delete()

    def test_pagination_get_page(self):
        ClientFactory.create_batch(size=51)
        for page, exp_page in [('0', 6), ('5', 5), ('43', 6), ('page', 1)]:
            response = self.view_client.get('/mock/', {'page': page})
            provider = ListViewFilterProvider(request=response.wsgi_request, model=Client)
            provider.paginate()
            self.assertEqual(provider.page_obj.number, exp_page)
        Client.objects.all().delete()

    def test_pagination_range(self):
        for pages_count, page_num, pages_range in [(5, 4, range(1, 6)), (10, 7, range(1, 11)),
                                                   (41, 17, range(7, 28)), (21, 12, range(2, 22)),
                                                   (2, None, range(1, 3)), ]:
            provider = ListViewFilterProvider(request=self.request, model=Client)
            self.assertEqual(provider._get_pagination_range(page_num=page_num, pages_count=pages_count), pages_range)

    def test_sorting_records(self):
        pass

    def test_sorting_order_by(self):
        pass

    def test_sorting_sort_by(self):
        pass

    """
    2. Sortowanie - TESTUJEMY W KONTEKSCIE SESSION KONIECZNIE!!
    - testujemy property sort_by i order by:
    --- order by: 
    -- 1. gdy przychodzi param asc/desc: aktualizujemy sesję o nowy param, zwracamy odpowiedni sort order
    ---2. gdy nie przychodzi nowy param: a) zwracamy to co jest w sesji; 
                                b) jeśli w sesji nie ma nic/nie ma tego klucza, zwracamy '' jako domyslny sort order
    --- sort by:
    -- 1. gdy przycohdzi nowy param sort_by: aktualizujemy sesję o nowy param, zwracamy ten param jako sort_by
    -- 2. gdy nie przychodzi nowy param: a) zwracamy to co jest w sesji; 
                                b) jesli w sesji nie ma nic/nie ma tego klucza, zwracamy domyslna wartosc sort_by 
                                (okreslona w modelu klasy)
    - testujemy sort_records: co sie stanie, jesli przyjdzie query string inny niz oczekiwany? Zabezpieczyć przed sytuacją
    podania w query stringu jakiegoś syfu!!! Również sql injection
    3. Filtrowanie
    -- Wkrótce
    """