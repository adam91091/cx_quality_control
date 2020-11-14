from django.template.defaulttags import register

from apps.template_filters import get_item_filter, get_pages_range_filter


@register.filter
def get_item(dictionary, key):
    return get_item_filter(dictionary, key)


@register.filter
def get_pages_range(current_page_num, pages_count):
    return get_pages_range_filter(current_page_num, pages_count)
