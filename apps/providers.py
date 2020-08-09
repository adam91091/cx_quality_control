from django.core.paginator import Paginator
from django.db.models import Q

from apps.clients.models import Client
from apps.products.models import Product

PAGINATION_LINKS_MAX_COUNT = 20
PAGINATION_OBJ_COUNT_PER_PAGE = 10


class ListViewFilterProvider:
    def __init__(self, request, model, fields=('client_name', 'client_sap_id')):
        self.request = request
        self.model = model
        self._order_by_asc = ''
        self._order_by_desc = '-'
        self._sort_by = 'id'  # implement method of get default sort key in model class
        self.fields = fields
        self._queryset = self._filter_queryset()
        self._page_obj = None
        self._pages_range = None

    @property
    def order_by(self):
        if self.request.GET.get('order_by') == self._order_by_asc:
            self.request.session['order_by'] = self._order_by_asc
            return self._order_by_asc
        elif self.request.GET.get('order_by') == self._order_by_desc:
            self.request.session['order_by'] = self._order_by_desc
            return self._order_by_desc
        else:
            return self.request.session.get('order_by', '')

    @property
    def sort_by(self):
        if self.request.GET.get('sort_by'):
            self._sort_by = self.request.GET.get('sort_by', 'id')
        else:
            self._sort_by = self.request.session.get('sort_by', 'id')
        self.request.session['sort_by'] = self._sort_by
        return self._sort_by

    @property
    def page_obj(self):
        return self._page_obj

    @property
    def pages_range(self):
        return self._pages_range

    def run(self):
        if self.request.GET.get('clear_filters') is None:
            self.sort_records()
        self.paginate()
        return self.request

    def sort_records(self):
        self._queryset = self._queryset.order_by(f'{self.order_by}{self.sort_by}')

    def queryset(self):
        return self._queryset

    def get_order_by_switch(self):
        return '' if self.order_by == '-' else '-'

    def _filter_queryset(self):
        if self.request.GET.get('clear_filters') is not None:
            for field_name in self.fields:
                self.request.session[field_name] = ""
            return self.model.objects.all().order_by('id')
        for field_name in self.fields:
            if self.request.GET.get(f'search-{field_name}') is not None:
                field_value = self.request.GET.get(f'search-{field_name}')
                self.request.session[field_name] = field_value
        return self._get_filter_query()

    def _get_filter_query(self):
        if self.model == Client:
            sap_id = self.request.session.get('client_sap_id', '')
            name = self.request.session.get('client_name', '')
            return self.model.objects.filter(Q(client_sap_id__char__icontains=sap_id) & Q(client_name__icontains=name))
        elif self.model == Product:
            sap_id = self.request.session.get('product_sap_id', '')
            index = self.request.session.get('index', '')
            desc = self.request.session.get('description', '')
            return self.model.objects.filter(Q(product_sap_id__char__icontains=sap_id) & Q(index__icontains=index) &
                                             Q(description__icontains=desc))

    def paginate(self):
        paginator = Paginator(self._queryset, PAGINATION_OBJ_COUNT_PER_PAGE)
        page_number = self._get_current_page_number()
        self._page_obj = paginator.get_page(page_number)
        self._pages_range = self._get_pagination_range(page_num=page_number,
                                                       pages_count=self._page_obj.paginator.num_pages)

    def _get_current_page_number(self):
        current_page = self.request.GET.get('page')
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
