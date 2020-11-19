import re
from typing import Union, List, Type

from betterforms.multiform import MultiForm
from django.contrib import messages
from django.contrib.sessions.backends.base import SessionBase
from django.forms import BaseForm
from django.http import QueryDict, HttpRequest

from apps.clients.filters import ClientFilter
from apps.orders.filters import OrderFilter
from apps.orders.models import Order
from apps.products.filters import ProductFilter


def add_error_messages(request: "HttpRequest", forms: List[Union["BaseForm", "MultiForm"]],
                       base_msg: str = "") -> None:
    """
    Parse error messages from forms and put it into django messages.
    :param request:     Django request instance
    :param forms:       form instances collection
    :param base_msg:    header of the error messages body
    """
    if base_msg:
        messages.error(request, base_msg)
    for form in forms:
        for err_msg in form.errors:
            cleaned = re.compile('<.*?>')
            msg = re.sub(cleaned, '', f"{err_msg}: {form.errors[err_msg]}")
            messages.error(request, msg)


def update_filter_params(params: "QueryDict", session: "SessionBase",
                         filter_class: Union[Type[ClientFilter], Type[ProductFilter],
                                             Type[OrderFilter]]) -> "SessionBase":
    """
    Update session for query parameters.
    Clear session when specific clear parameter occurs.
    :param params:       request query parameters
    :param session:      Django session reference
    :param filter_class: filter class reference
    :return session:     reference for updated session
    """
    for param in params:
        param_val = params.get(param)
        if param_val is not None:
            session[param] = param_val
    if 'clear_filters' in params:
        for field_name in filter_class.get_fields():
            session[field_name] = ''
        if filter_class == OrderFilter:
            session['date_of_production_after'] = Order.get_date_of_production('today')
            session['date_of_production_before'] = Order.get_date_of_production('max')
    return session


def update_ordering(params: "QueryDict", session: "SessionBase") -> "SessionBase":
    """
    Update session for ordering query parameter.
    Clear session when specific clear parameter occurs.
    :param params:       request query parameters
    :param session:      Django session reference
    :return session:     reference for updated session
    """
    ordering = params.get('ordering')
    if ordering is not None:
        session['ordering'] = ordering
    if 'clear_filters' in params:
        session['ordering'] = 'id'
    return session
