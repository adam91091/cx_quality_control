import re

from django.contrib import messages


def add_error_messages(request, main_msg, form, secondary_forms=None):
    messages.error(request, main_msg)
    for err_msg in form.errors:
        messages.error(request, form.errors[err_msg])
    if secondary_forms is not None:
        for form in secondary_forms:
            for err_msg in form.errors:
                cleaned = re.compile('<.*?>')
                msg = re.sub(cleaned, '', f"{err_msg}: {form.errors[err_msg]}")
                messages.error(request, msg)
