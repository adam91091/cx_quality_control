import django_filters

from apps.products.models import Product


class ProductFilter(django_filters.FilterSet):
    product_sap_id = django_filters.CharFilter(lookup_expr='icontains')
    index = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ('product_sap_id', 'index', 'description', )
