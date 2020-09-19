import datetime
from django.contrib.sessions.backends.base import SessionBase
from django.core.paginator import Paginator
from django.db.models import Q

from apps.clients.models import Client
from apps.orders.models import Order
from apps.products.models import Product

PAGINATION_LINKS_MAX_COUNT = 20
PAGINATION_OBJ_COUNT_PER_PAGE = 10

MIN_DATE = '0001-01-01'
MAX_DATE = '9999-12-31'


class FilterProvider:
    def __init__(self, model, session, params: dict):
        self.model = model
        self.session = session
        self.params = params
        self.filters = self._get_filters()

    def get_queryset(self):
        """Get queryset filtered by keyword values from session"""
        self._update_session()
        if self.model == Client:
            return self.model.objects.filter(Q(client_sap_id__char__icontains=self.session.get('client_sap_id', '')) &
                                             Q(client_name__icontains=self.session.get('client_name', '')))
        elif self.model == Product:
            return self.model.objects.filter(Q(product_sap_id__char__icontains=self.session.get('product_sap_id', '')) &
                                             Q(index__icontains=self.session.get('index', '')) &
                                             Q(description__icontains=self.session.get('description', '')))
        elif self.model == Order:
            return self.model.objects.filter(Q(client__client_name__icontains=self.session.get('client_name', '')) &
                                             Q(order_sap_id__char__icontains=self.session.get('order_sap_id', '')) &
                                             Q(product__product_sap_id__char__icontains=self.session.get('product_sap_id', '')) &
                                             Q(status__icontains=self.session.get('status', '')) &
                                             Q(product__description__icontains=self.session.get('description', '')) &
                                             Q(date_of_production__range=(self.session.get('start_date', MIN_DATE),
                                                                          self.session.get('end_date', MAX_DATE)))
                                             )

    def _get_filters(self):
        """Get model filters from previous session state"""
        filters = {}
        if self.model == Product:
            filters = {'product_sap_id': self.session.get('product_sap_id', ''),
                       'index': self.session.get('index', ''),
                       'description': self.session.get('description', '')}
        elif self.model == Client:
            filters = {'client_sap_id': self.session.get('client_sap_id', ''),
                       'client_name': self.session.get('client_name', '')}
        elif self.model == Order:
            filters = {'order_sap_id': self.session.get('order_sap_id', ''),
                       'client_name': self.session.get('client_name', ''),
                       'product_sap_id': self.session.get('product_sap_id', ''),
                       'start_date': self.session.get('start_date', MIN_DATE),
                       'end_date': self.session.get('end_date', MAX_DATE),
                       'status': self.session.get('status', ''),
                       'description': self.session.get('description', '')}

        return filters

    def _update_session(self):
        """Update session for incoming params if any filter is present"""
        for filter_name in self.filters:
            if 'clear_filters' in self.params:
                self.session[filter_name] = ""
            else:
                if f'search-{filter_name}' in self.params:
                    self.session[filter_name] = self.params[f'search-{filter_name}']
                elif f'search_{filter_name}' in self.params:
                    self.session[filter_name] = self.params[f'search_{filter_name}']
        # set dates if are empty in params
        if 'start_date' in self.session and self.session['start_date'] == '':
            self.session['start_date'] = MIN_DATE
        if 'end_date' in self.session and self.session['end_date'] == '':
            self.session['end_date'] = MAX_DATE


class PaginationProvider:
    def __init__(self, queryset, page: int):
        self.queryset = queryset
        self.page = page

    def paginate(self) -> tuple:
        paginator = Paginator(self.queryset, PAGINATION_OBJ_COUNT_PER_PAGE)
        page_number = self._get_current_page_number()
        page_obj = paginator.get_page(page_number)
        pages_range = self._get_pagination_range(page_num=page_number,
                                                 pages_count=page_obj.paginator.num_pages)
        return page_obj, pages_range

    def _get_current_page_number(self):
        current_page = self.page
        try:
            page_num = int(current_page)
        except (ValueError, TypeError):
            page_num = 1
        return page_num

    @staticmethod
    def _get_pagination_range(page_num, pages_count):
        if pages_count <= PAGINATION_LINKS_MAX_COUNT:
            pages_range = range(1, pages_count + 1)
        else:
            if page_num <= (PAGINATION_LINKS_MAX_COUNT // 2):
                pages_range = range(1, PAGINATION_LINKS_MAX_COUNT + 1)
            elif page_num >= pages_count - (PAGINATION_LINKS_MAX_COUNT // 2):
                pages_range = range(pages_count - (PAGINATION_LINKS_MAX_COUNT - 1), pages_count + 1)
            else:
                pages_range = range(page_num - (PAGINATION_LINKS_MAX_COUNT // 2),
                                    page_num + (PAGINATION_LINKS_MAX_COUNT // 2 + 1))
        return pages_range


class SortingProvider:
    def __init__(self, model, session, params):
        self.model = model
        self.session = session
        self.params = params
        self.order_by = self._get_order_by_direction()
        self.sort_by = self._get_sort_by_name()

    def sort_queryset(self, queryset):
        order_related_keywords = {'client_name': 'client', 'product_sap_id': 'product', 'description': 'product'}
        order_by = '-' if self.order_by == 'desc' else ''
        if self.model == Order and self.sort_by in order_related_keywords:
            return queryset.order_by(f'{order_by}{order_related_keywords[self.sort_by]}__{self.sort_by}')
        else:
            return queryset.order_by(f'{order_by}{self.sort_by}')

    def get_next_order_by(self):
        next_order_by_dict = {'asc': 'desc', 'desc': 'asc'}
        next_order_by = next_order_by_dict.get(self.order_by, self.session.get('order_by', 'asc'))
        return next_order_by

    def _get_sort_by_name(self):
        """Update session if sort_by params """
        model_sort_names = {'Client': ('client_sap_id', 'client_name'),
                            'Product': ('product_sap_id', 'description', 'index'),
                            'Order': ('order_sap_id', 'client_name', 'product_sap_id', 'date_of_production', 'status',
                                      'description')}

        # Update session for incoming params if are valid
        if 'sort_by' in self.params:
            if self.params['sort_by'] in model_sort_names.get(self.model.__name__, ()):
                self.session['sort_by'] = self.params['sort_by']

        # Clear sort by If clear filters is present in params or
        # existing sort_by in session is not valid for current model
        if 'clear_filters' in self.params or self.session.get('sort_by', 'id') not in \
                model_sort_names.get(self.model.__name__, ()):
            self.session['sort_by'] = 'id'

        return self.session.get('sort_by', 'id')

    def _get_order_by_direction(self):
        if 'order_by' in self.params:
            if self.params['order_by'] in ('asc', 'desc'):
                self.session['order_by'] = self.params['order_by']

        if 'clear_filters' in self.params:
            self.session['order_by'] = 'asc'

        return self.session.get('order_by', 'asc')
