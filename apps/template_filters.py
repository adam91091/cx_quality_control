from typing import Hashable

from apps.constants import PAGINATION_LINKS_MAX_COUNT


def get_item_filter(dictionary: dict, key: Hashable) -> str:
    """Provide accessing values from dict inside template"""
    try:
        return dictionary.get(key)
    except AttributeError:
        pass


def get_pages_range_filter(current_page_num: int, pages_count: int) -> range:
    """
    Provide max link amount of active pages for paginator.
    :param current_page_num:    currently displayed page pagination index
    :param pages_count:         total pages number consistent with objects count in db
    :return pages_range:        pages links range
    """
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
