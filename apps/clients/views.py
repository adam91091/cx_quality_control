from django.shortcuts import render, redirect
from django.contrib import messages

from apps.clients.forms import ClientForm
from apps.clients.models import Client
from apps.view_utils import add_error_messages


def clients_list(request):
    clients = Client.objects.all()
    return render(request, 'clients_list.html', {'clients': clients})


def client_new(request):
    if request.method == 'POST':
        client_form = ClientForm(request.POST)
        if client_form.is_valid():
            client = client_form.save(commit=False)
            client.save()
            messages.success(request, 'Utworzono nowego klienta')
            return redirect('clients:clients_list')
        else:
            add_error_messages(request, main_msg="Nie utworzono nowego klienta. "
                                                 "Wystąpiły następujące błędy formularza:",
                               form=client_form)
            return render(request, 'client_form.html', {'client_form': client_form, 'type': 'new'})
    else:
        client_form = ClientForm()
        return render(request, 'client_form.html', {'client_form': client_form, 'type': 'new'})


def client_delete(request, client_id):
    client = Client.objects.get(id=client_id)
    if request.method == 'POST':
        client.delete()
        messages.success(request, f"Klient został usunięty")
        return redirect('clients:clients_list')
    else:
        return render(request, 'client_confirm_delete.html', {'client': client})


def client_update(request, client_id):
    client = Client.objects.get(id=client_id)
    if request.method == 'POST':
        client_form = ClientForm(request.POST, instance=client)
        if client_form.is_valid():
            client = client_form.save(commit=False)
            client.save()
            messages.success(request, f'Zaktualizowano dane klienta')
            return redirect('clients:clients_list')
        else:
            add_error_messages(request, main_msg="Nie zaktualizowano danych klienta. "
                                                 "Wystąpiły następujące błędy formularza:",
                               form=client_form)
            return render(request, 'client_form.html', {'client_form': client_form, 'type': 'update'})

    else:
        client_form = ClientForm(instance=client)
        return render(request, 'client_form.html', {'client_form': client_form, 'type': 'update'})
