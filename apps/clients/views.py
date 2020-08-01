from django.shortcuts import render, redirect
from django.contrib import messages

from apps.clients.forms import ClientForm
from apps.clients.models import Client
from apps.views_utils import VIEW_MSG, render_form_response
from apps.providers import ListViewFilterProvider


def clients_list(request):
    client_provider = ListViewFilterProvider(request=request, model=Client)
    request = client_provider.run()
    return render(request, 'clients_list.html', {'page_obj': client_provider.page_obj,
                                                 'pages_range': client_provider.pages_range,
                                                 'order_by': client_provider.get_order_by_switch()})


def client_delete(request, client_id):
    client = Client.objects.get(id=client_id)
    if request.method == 'POST':
        client.delete()
        messages.success(request, VIEW_MSG['client']['delete'])
        return redirect('clients:clients_list')
    else:
        return render(request, 'client_confirm_delete.html', {'client': client})


def client_new(request):
    if request.method == 'POST':
        client_form = ClientForm(request.POST)
    else:
        client_form = ClientForm()
    return render_form_response(request=request, method='new', form=client_form, model_name='client')


def client_update(request, client_id):
    client = Client.objects.get(id=client_id)
    if request.method == 'POST':
        client_form = ClientForm(request.POST, instance=client)
    else:
        client_form = ClientForm(instance=client)
    return render_form_response(request=request, method='update', form=client_form, model_name='client')
