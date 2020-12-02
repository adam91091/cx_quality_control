from django.contrib import messages
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy

from apps.clients.filters import ClientFilter
from apps.clients.forms import ClientForm
from apps.clients.models import Client
from apps.constants import PAGINATION_OBJ_COUNT_PER_PAGE
from apps.user_texts import VIEW_MSG
from apps.view_helpers import add_error_messages, update_filter_params, update_ordering


class ClientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """List clients, provide client filtering and sorting."""
    model = Client
    template_name = 'clients_list.html'
    login_url = 'users:user-login'
    permission_required = ('clients.view_client', )
    paginate_by = PAGINATION_OBJ_COUNT_PER_PAGE
    ordering = ('id', )

    def get_queryset(self):
        """Update session for request GET parameters.
        Filter & sort clients by parameters values stored in session.
        """
        self.request.session = update_filter_params(params=self.request.GET,
                                                    session=self.request.session,
                                                    filter_class=ClientFilter)
        client_filter = ClientFilter(self.request.session, queryset=self.model.objects.all())
        qs = client_filter.qs.order_by(self.get_ordering())
        return qs

    def get_ordering(self):
        """Update session for ordering parameter from request.
        Return ordering value stored in session or id as a default.
        """
        self.request.session = update_ordering(params=self.request.GET,
                                               session=self.request.session)
        return self.request.session.get('ordering', 'id')


class ClientCreateView(SuccessMessageMixin, LoginRequiredMixin,
                       PermissionRequiredMixin, CreateView):
    """Create a new client in database using client form."""
    form_class = ClientForm
    template_name = 'client_form.html'
    login_url = 'users:user-login'
    permission_required = ('clients.add_client', )
    success_url = reverse_lazy('clients:clients-list')
    success_message = VIEW_MSG['client']['new_success']

    def form_invalid(self, form):
        add_error_messages(request=self.request, forms=[form, ],
                           base_msg=VIEW_MSG['client']['new_error'])
        return super().form_invalid(form)


class ClientDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Provide information about client."""
    model = Client
    template_name = 'client_detail.html'
    login_url = 'users:user-login'
    permission_required = ('clients.view_client', )


class ClientUpdateView(SuccessMessageMixin, LoginRequiredMixin,
                       PermissionRequiredMixin, UpdateView):
    """Update client in database using client form."""
    model = Client
    form_class = ClientForm
    template_name = 'client_form.html'
    login_url = 'users:user-login'
    permission_required = ('clients.change_client', )
    success_url = reverse_lazy('clients:clients-list')
    success_message = VIEW_MSG['client']['update_success']

    def form_invalid(self, form):
        add_error_messages(request=self.request, forms=[form, ],
                           base_msg=VIEW_MSG['client']['update_error'])
        return super().form_invalid(form)


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Delete client from database.
    All orders referenced to this client are also deleted.
    """
    model = Client
    template_name = 'client_confirm_delete.html'
    login_url = 'users:user-login'
    permission_required = ('clients.delete_client', )
    success_url = reverse_lazy('clients:clients-list')
    success_message = VIEW_MSG['client']['delete_success']

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
