from django.template.defaulttags import register

from apps.globals import PAGINATION_LINKS_MAX_COUNT


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_pages_range(current_page_num, pages_count):
    if pages_count <= PAGINATION_LINKS_MAX_COUNT:
        pages_range = range(1, pages_count + 1)
    else:
        if current_page_num <= (PAGINATION_LINKS_MAX_COUNT // 2):
            pages_range = range(1, PAGINATION_LINKS_MAX_COUNT + 1)
        elif current_page_num >= pages_count - (PAGINATION_LINKS_MAX_COUNT // 2):
            pages_range = range(pages_count - (PAGINATION_LINKS_MAX_COUNT - 1), pages_count + 1)
        else:
            pages_range = range(current_page_num - (PAGINATION_LINKS_MAX_COUNT // 2),
                                current_page_num + (PAGINATION_LINKS_MAX_COUNT // 2 + 1))
    return pages_range
