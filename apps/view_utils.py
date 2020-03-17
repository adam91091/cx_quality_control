from django.contrib import messages


def add_error_messages(request, main_msg, form):
    messages.error(request, main_msg)
    for err_msg in form.errors:
        messages.error(request, form.errors[err_msg])
