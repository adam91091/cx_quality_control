from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy

from apps.clients.filters import ClientFilter
from apps.clients.forms import ClientForm
from apps.clients.models import Client
from apps.providers import PAGINATION_OBJ_COUNT_PER_PAGE
from apps.views_utils import VIEW_MSG, add_error_messages


class ClientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Client
    template_name = 'clients_list.html'
    permission_required = ('clients.view_client', )
    login_url = 'users:user_login'
    paginate_by = PAGINATION_OBJ_COUNT_PER_PAGE
    ordering = ('id', )

    def get_queryset(self):
        for param in self.request.GET:
            param_val = self.request.GET.get(param)
            if param_val is not None:
                self.request.session[param] = param_val
        if 'clear_filters' in self.request.GET:
            for field_name in ClientFilter.get_fields():
                self.request.session[field_name] = ''

        client_filter = ClientFilter(self.request.session, queryset=self.model.objects.all())
        qs = client_filter.qs.order_by(self.get_ordering())
        return qs

    def get_ordering(self):
        ordering = self.request.GET.get('ordering')
        if ordering is not None:
            self.request.session['ordering'] = ordering
        if 'clear_filters' in self.request.GET:
            self.request.session['ordering'] = 'id'
        return self.request.session.get('ordering', 'id')


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
