from django.http import HttpResponse
from django.shortcuts import render, redirect

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
            return redirect('clients:clients_list')
        else:
            return HttpResponse(status=500)
    else:
        client_form = ClientForm()
    return render(request, 'client_form.html', {'client_form': client_form})


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
            return redirect('clients:clients_list')
        else:
            return HttpResponse(status=500)
    else:
        client_form = ClientForm(instance=client)
    return render(request, 'client_form.html', {'client_form': client_form})
