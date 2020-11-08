from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required, login_required

from apps.clients.forms import ClientForm
from apps.clients.models import Client
from apps.views_utils import VIEW_MSG, add_error_messages
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


class ClientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Client
    template_name = 'clients_list.html'
    permission_required = ('clients.view_client', )
    login_url = 'users:user_login'


class ClientDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Client
    template_name = 'client_detail.html'
    permission_required = ('clients.view_client', )
    login_url = 'users:user_login'


class ClientDeleteView(SuccessMessageMixin, LoginRequiredMixin,
                       PermissionRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('clients:clients-list')
    template_name = 'client_confirm_delete.html'
    permission_required = ('clients.delete_client', )
    success_message = VIEW_MSG['client']['delete_success']
    login_url = 'users:user_login'


class ClientCreateView(SuccessMessageMixin, LoginRequiredMixin,
                       PermissionRequiredMixin, CreateView):
    form_class = ClientForm
    template_name = 'client_form.html'
    permission_required = ('clients.add_client', )
    login_url = 'users:user_login'
    success_url = reverse_lazy('clients:clients-list')
    success_message = VIEW_MSG['client']['new_success']

    def form_invalid(self, form):
        add_error_messages(self.request, VIEW_MSG['client']['new_error'], form)
        return super().form_invalid(form)


class ClientUpdateView(SuccessMessageMixin, LoginRequiredMixin,
                       PermissionRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'client_form.html'
    permission_required = ('clients.change_client', )
    login_url = 'users:user_login'
    success_url = reverse_lazy('clients:clients-list')
    success_message = VIEW_MSG['client']['update_success']

    def form_invalid(self, form):
        add_error_messages(self.request, VIEW_MSG['client']['update_error'], form)
        return super().form_invalid(form)
