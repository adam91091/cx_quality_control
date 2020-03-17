from django.shortcuts import render, redirect
from django.contrib import messages

from apps.clients.forms import ClientForm
from apps.clients.models import Client


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
        else:
            messages.error(request, 'Wystąpił błąd formularza. Nie utworzono nowego klienta')
        return redirect('clients:clients_list')
    else:
        client_form = ClientForm()
        return render(request, 'client_form.html', {'client_form': client_form, 'type': 'new'})


def client_delete(request, client_id):
    client = Client.objects.get(id=client_id)
    if request.method == 'POST':
        client.delete()
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
        else:
            messages.error(request, 'Wystąpił błąd formularza. Nie zaktualizowano danych klienta')
        return redirect('clients:clients_list')

    else:
        client_form = ClientForm(instance=client)
        return render(request, 'client_form.html', {'client_form': client_form, 'type': 'update'})
