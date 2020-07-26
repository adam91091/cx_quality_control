from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator

from apps.clients.forms import ClientForm
from apps.clients.models import Client
from apps.views_utils import VIEW_MSG, render_form_response, get_pagination_range, PAGINATION_OBJ_COUNT_PER_PAGE


def clients_list(request):
    clients = Client.objects.all().order_by('id')
    paginator = Paginator(clients, PAGINATION_OBJ_COUNT_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    pages_range = get_pagination_range(page_num=page_number, pages_count=paginator.num_pages)
    return render(request, 'clients_list.html', {'page_obj': page_obj, 'pages_range': pages_range})


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
