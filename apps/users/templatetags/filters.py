from django.template.defaulttags import register

from apps.template_filters import get_item_filter


@register.filter
def get_item(dictionary, key):
    return get_item_filter(dictionary, key)
