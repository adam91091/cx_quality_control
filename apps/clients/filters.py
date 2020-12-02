import django_filters

from apps.clients.models import Client


class ClientFilter(django_filters.FilterSet):
    client_name = django_filters.CharFilter(lookup_expr='icontains')
    client_sap_id = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Client
        fields = ('client_name', 'client_sap_id')
