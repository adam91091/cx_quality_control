from django.test import TestCase

from apps.clients.models import Client
from apps.clients.tests.factories import ClientFactory
from apps.providers import FilterProvider, PaginationProvider, PAGINATION_OBJ_COUNT_PER_PAGE, SortingProvider


class PaginationProviderTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        pass

    def test_pagination_basic(self):
        for obj_num, num_pages in [(31, 4), (7, 1)]:
            ClientFactory.create_batch(size=obj_num)
            queryset = Client.objects.all()
            provider = PaginationProvider(page=obj_num, queryset=queryset)
            page_obj, _ = provider.paginate()
            self.assertEqual(page_obj.paginator.num_pages, num_pages)
            Client.objects.all().delete()

    def test_pagination_get_page(self):
        ClientFactory.create_batch(size=51)
        queryset = Client.objects.all()
        for page, exp_page in [(0, 6), (5, 5), (43, 6)]:
            provider = PaginationProvider(page=page, queryset=queryset)
            page_obj, _ = provider.paginate()
            self.assertEqual(page_obj.number, exp_page)
        Client.objects.all().delete()

    def test_pagination_range(self):
        for pages_count, page_num, exp_pages_range in [(5, 4, range(1, 6)), (10, 7, range(1, 11)),
                                                       (41, 17, range(7, 28)), (21, 12, range(2, 22)),
                                                       (2, None, range(1, 3)), ]:
            ClientFactory.create_batch(size=pages_count * PAGINATION_OBJ_COUNT_PER_PAGE)
            queryset = Client.objects.all()
            provider = PaginationProvider(page=page_num, queryset=queryset)
            _, pages_range = provider.paginate()
            self.assertEqual(pages_range, exp_pages_range)
            Client.objects.all().delete()


class SortingProviderTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        ClientFactory.create_batch(size=51)
        cls.queryset = Client.objects.all()

    def test_sorting_basic(self):
        provider = SortingProvider(model=Client, session={'sort_by': 'client_name', 'order_by': 'asc'},
                                   params={'sort_by': 'client_sap_id', 'order_by': 'desc'})
        sorted_queryset = provider.sort_queryset(self.queryset)
        self.assertEqual(list(sorted_queryset), list(self.queryset.order_by('-client_sap_id')))

    def test_sorting_negative_params(self):
        provider = SortingProvider(model=Client, session={'sort_by': 'client_name', 'order_by': 'desc'},
                                   params={'sort_by': 'wrong_param!', 'order_by': 'wrong_order!'})
        sorted_queryset = provider.sort_queryset(self.queryset)
        self.assertEqual(list(sorted_queryset), list(self.queryset.order_by('-client_name')))

    def test_sorting_negative_session(self):
        provider = SortingProvider(model=Client, session={'sort_by': 'wrong_param!', 'order_by': 'wrong_order!'},
                                   params={})
        sorted_queryset = provider.sort_queryset(self.queryset)
        self.assertEqual(list(sorted_queryset), list(self.queryset.order_by('id')))

    def test_sorting_next_order_by(self):
        provider = SortingProvider(model=Client, session={'sort_by': 'client_name', 'order_by': 'desc'},
                                   params={'sort_by': 'client_sap_id', 'order_by': 'asc'})
        next_order_by = provider.get_next_order_by()
        self.assertEqual(next_order_by, 'desc')


class FilterProviderTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        ClientFactory.create_batch(size=16)
        cls.queryset = Client.objects.all()

    def test_filter_basic(self):
        provider = FilterProvider(model=Client, session={'search-client_name': 'client',
                                                         },
                                  params={})
        queryset = provider.get_queryset()
        self.assertEqual(list(queryset), list(self.queryset.all()))
