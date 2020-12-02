import django_filters

from apps.orders.models import Order


class OrderFilter(django_filters.FilterSet):
    client_name = django_filters.CharFilter(field_name='client__client_name', lookup_expr='icontains')
    order_sap_id = django_filters.CharFilter(lookup_expr='icontains')
    product_sap_id = django_filters.CharFilter(field_name='product__product_sap_id', lookup_expr='icontains')
    date_of_production = django_filters.DateTimeFromToRangeFilter(lookup_expr='range')
    description = django_filters.CharFilter(field_name='product__description', lookup_expr='icontains')
    status = django_filters.ChoiceFilter(choices=Order.STATUS_CHOICES, lookup_expr='iexact')

    class Meta:
        model = Order
        fields = ('client_name', 'order_sap_id', 'product_sap_id',
                  'date_of_production', 'description', 'status', )
