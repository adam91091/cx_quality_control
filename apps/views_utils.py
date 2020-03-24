from django.contrib import messages

VIEW_MSG = {'client': {'new_success': "Utworzono nowego klienta",
                       'new_error': "Nie utworzono nowego klienta. "
                                    "Wystąpiły następujące błędy formularza:",
                       'update_success': "Zaktualizowano dane klienta",
                       'update_error': "Nie zaktualizowano danych klienta. "
                                       "Wystąpiły następujące błędy formularza:",
                       'delete': "Klient został usunięty", },
            }


def add_error_messages(request, main_msg, form):
    messages.error(request, main_msg)
    for err_msg in form.errors:
        messages.error(request, form.errors[err_msg])
