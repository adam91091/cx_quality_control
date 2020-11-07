from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import permission_required, login_required

from apps.clients.forms import ClientForm
from apps.clients.models import Client
from apps.views_utils import VIEW_MSG, render_form_response
from apps.providers import FilterProvider, PaginationProvider, SortingProvider


@login_required
@permission_required("clients.view_client")
def clients_list(request):
    client_filter_provider = FilterProvider(model=Client, session=request.session, params=request.GET)
    clients = client_filter_provider.get_queryset()

    client_sorting_provider = SortingProvider(model=Client, session=request.session, params=request.GET)
    clients = client_sorting_provider.sort_queryset(queryset=clients)
    order_by = client_sorting_provider.get_next_order_by()

    client_pagination_provider = PaginationProvider(queryset=clients, page=request.GET.get('page', 1))
    page_obj, pages_range = client_pagination_provider.paginate()

    return render(request, 'clients_list.html', {'page_obj': page_obj,
                                                 'pages_range': pages_range,
                                                 'order_by': order_by})


@login_required
@permission_required("clients.view_client")
def client_detail(request, client_id):
    client = Client.objects.get(id=client_id)
    client_form = ClientForm(instance=client, read_only=True)
    return render(request, 'client_form.html', {'client_form': client_form, 'type': 'detail'})


@login_required
@permission_required("clients.delete_client")
def client_delete(request, client_id):
    client = Client.objects.get(id=client_id)
    if request.method == 'POST':
        client.delete()
        messages.success(request, VIEW_MSG['client']['delete'])
        return redirect('clients:clients_list')
    else:
        return render(request, 'client_confirm_delete.html', {'client': client})


@login_required
@permission_required("clients.add_client")
def client_new(request):
    if request.method == 'POST':
        client_form = ClientForm(data=request.POST)
    else:
        client_form = ClientForm()
    return render_form_response(request=request, method='new', form=client_form, model_name='client')


@login_required
@permission_required("clients.change_client")
def client_update(request, client_id):
    client = Client.objects.get(id=client_id)
    if request.method == 'POST':
        client_form = ClientForm(data=request.POST, instance=client, update=True)
    else:
        client_form = ClientForm(instance=client, update=True)
    return render_form_response(request=request, method='update', form=client_form, model_name='client')
