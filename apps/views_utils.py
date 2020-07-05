import re

from django.contrib import messages
from django.shortcuts import redirect, render

VIEW_MSG = {'client': {'new_success': "Utworzono nowego klienta",
                       'new_error': "Nie utworzono nowego klienta. "
                                    "Wystąpiły następujące błędy formularza:",
                       'update_success': "Zaktualizowano dane klienta",
                       'update_error': "Nie zaktualizowano danych klienta. "
                                       "Wystąpiły następujące błędy formularza:",
                       'delete': "Klient został usunięty", },
            'product': {'new_success': "Utworzono nowy produkt",
                        'new_error': "Nie utworzono nowego produktu. "
                                     "Wystąpiły następujące błędy formularza:",
                        'update_success': "Zaktualizowano dane produktu",
                        'update_error': "Nie zaktualizowano danych produktu",
                        'delete': "Produkt został usunięty", },
            'order': {'new_success': "Utworzono nowe zlecenie produkcyjne",
                      'new_error': "Nie utworzono nowego zlecenia produkcyjnego. "
                                   "Wystąpiły następujące błędy formularza:",
                      'update_success': "Zaktualizowano dane zlecenia produkcyjnego",
                      'update_error': "Nie zaktualizowano danych zlecenia produkcyjnego. "
                                      "Wystąpiły następujące błędy formularza:",
                      'delete': "Zlecenie produkcyjne zostało usunięte", },
            'measurement_report': {'new_success': "Dodano raport pomiarowy",
                                   'new_error': "Raport pomiarowy nie został dodany. "
                                                "Wystąpiły następujące błędy formularza:",
                                   'update_success': "Zaktualizowano raport pomiarowy",
                                   'update_error': "Nie zaktualizowano raportu pomiarowego. "
                                                   "Wystąpiły następujące błędy formularza:", },
            }


def add_error_messages(request, main_msg, form, secondary_forms=None):
    messages.error(request, main_msg)
    for err_msg in form.errors:
        messages.error(request, form.errors[err_msg])
    if secondary_forms is not None:
        for form in secondary_forms:
            for err_msg in form.errors:
                cleanr = re.compile('<.*?>')
                msg = re.sub(cleanr, '', f"{err_msg}: {form.errors[err_msg]}")
                messages.error(request, msg)


def render_form_response(request, method, form, model_name):
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, VIEW_MSG[model_name][f'{method}_success'])
        return redirect(f'{model_name}s:{model_name}s_list')
    if request.method == 'POST':
        add_error_messages(request, main_msg=VIEW_MSG[model_name][f'{method}_error'],
                           form=form)
    return render(request, f'{model_name}_form.html', {f'{model_name}_form': form, 'type': method})


def render_one_to_one_form_response(request, method, parent_form, child_form, parent_name, child_name):
    if parent_form.is_valid() and child_form.is_valid():
        parent = parent_form.save(commit=False)
        parent.save()
        messages.success(request, VIEW_MSG[parent_name][f'{method}_success'])
        child = child_form.save(commit=False)
        setattr(child, parent_name, parent)
        child.save()
        return redirect(f'{parent_name}s:{parent_name}s_list')
    if request.method == 'POST':
        add_error_messages(request, main_msg=VIEW_MSG[parent_name][f'{method}_error'], form=parent_form,
                           secondary_forms=[child_form, ])
    return render(request, f'{parent_name}_form.html', {f'{parent_name}_form': parent_form,
                                                        f'{child_name}_form': child_form,
                                                        'type': method})


def check_if_related_object_exists(request, model, sap_id_name, sap_id_value, model_name):
    try:
        obj = model.objects.get(**{sap_id_name: sap_id_value})
    except model.DoesNotExist:
        messages.error(request, f"Operacja anulowana. "
                                f"{model_name} o numerze SAP: {sap_id_value}  nie istnieje w bazie danych")
        return None
    return obj
