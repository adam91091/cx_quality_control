from django.core.paginator import Paginator
from django.db.models import Q

from apps.clients.models import Client

PAGINATION_LINKS_MAX_COUNT = 20
PAGINATION_OBJ_COUNT_PER_PAGE = 10


def get_pagination_range(page_num, pages_count):
    if page_num is None:
        return range(1, pages_count + 1)
    try:
        page_num = int(page_num)
    except ValueError:
        pages_range = range(1, pages_count + 1)
        return pages_range

    if pages_count < PAGINATION_LINKS_MAX_COUNT:
        pages_range = range(1, pages_count + 1)
    else:
        if page_num <= 5:
            pages_range = range(1, PAGINATION_LINKS_MAX_COUNT + 1)
        elif page_num >= pages_count - (PAGINATION_LINKS_MAX_COUNT // 2):
            pages_range = range(pages_count - (PAGINATION_LINKS_MAX_COUNT - 1), pages_count + 1)
        else:
            pages_range = range(page_num - (PAGINATION_LINKS_MAX_COUNT // 2),
                                page_num + (PAGINATION_LINKS_MAX_COUNT // 2 + 1))
    return pages_range


class ListViewFilterProvider:
    def __init__(self, request, model):
        self.request = request
        self.model = model
        self._order_by_asc = ''
        self._order_by_desc = '-'
        self._sort_by = 'id'  # implement method of get default sort key in model class
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
            return self.request.session['order_by']

    @property
    def sort_by(self):
        self._sort_by = self.request.GET.get('sort_by') if self.request.GET.get('sort_by') \
                                                        else self.request.session.get('sort_by')
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
            for field in self.model._meta.get_fields():
                self.request.session[field.name] = ""
            return self.model.objects.all()
        for field in self.model._meta.get_fields():
            if self.request.GET.get(f'search-{field.name}') is not None:
                field_value = self.request.GET.get(f'search-{field.name}')
                self.request.session[field.name] = field_value
        return self._get_filter_query()

    def _get_filter_query(self):
        if self.model == Client:
            return self.model.objects.filter(Q(client_sap_id__char__icontains=self.request.session['client_sap_id']) &
                                             Q(client_name__icontains=self.request.session['client_name']))

    def paginate(self):
        paginator = Paginator(self._queryset, PAGINATION_OBJ_COUNT_PER_PAGE)
        page_number = self.request.GET.get('page')
        self._page_obj = paginator.get_page(page_number)
        self._pages_range = get_pagination_range(page_num=page_number, pages_count=paginator.num_pages)
