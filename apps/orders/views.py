from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView, FormView

from apps.constants import PAGINATION_OBJ_COUNT_PER_PAGE
from apps.user_texts import VIEW_MSG
from .filters import OrderFilter
from .forms import OrderForm, MeasurementFormSet, MeasurementReportForm, DateFilteringForm
from .models import Order, MeasurementReport
from apps.view_helpers import add_error_messages, update_ordering, update_filter_params


class OrderListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """List orders, provide order filtering and sorting"""
    model = Order
    template_name = 'orders_list.html'
    login_url = 'users:user-login'
    permission_required = ('orders.view_order', )
    paginate_by = PAGINATION_OBJ_COUNT_PER_PAGE
    ordering = ('id', )

    def get_queryset(self):
        """Update session for request GET parameters.
        Filter & sort orders by parameters values stored in session.
        """
        self.request.session = update_filter_params(params=self.request.GET,
                                                    session=self.request.session,
                                                    filter_class=OrderFilter)
        order_filter = OrderFilter(self.request.session, queryset=self.model.objects.all())
        qs = order_filter.qs.order_by(self.get_ordering())
        return qs

    def get_context_data(self, **kwargs):
        """Update context for data required by date filter."""
        context = super().get_context_data(**kwargs)
        date_filtering_form = DateFilteringForm(initial={
            'date_of_production_after': self.request.session.get('date_of_production_after'),
            'date_of_production_before': self.request.session.get('date_of_production_before'), })
        context['date_filtering_form'] = date_filtering_form
        return context

    def get_ordering(self):
        """Update session for ordering parameter from request.
        Return ordering value stored in session or id as a default.
        """
        self.request.session = update_ordering(params=self.request.GET,
                                               session=self.request.session)
        return self.request.session.get('ordering', 'id')


class OrderCreateView(SuccessMessageMixin, LoginRequiredMixin,
                      PermissionRequiredMixin, CreateView):
    """Create a new order in database using order form.
    Requires references for existing product & client.
    """
    form_class = OrderForm
    template_name = 'order_form.html'
    login_url = 'users:user-login'
    permission_required = ('orders.add_order', )
    success_url = reverse_lazy('orders:orders-list')
    success_message = VIEW_MSG['order']['new_success']

    def form_invalid(self, form):
        add_error_messages(request=self.request, forms=[form, ],
                           base_msg=VIEW_MSG['order']['new_error'])
        return super().form_invalid(form)


class OrderDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Provide information about order."""
    model = Order
    template_name = 'order_detail.html'
    login_url = 'users:user-login'
    permission_required = ('orders.view_order', )


class OrderUpdateView(SuccessMessageMixin, LoginRequiredMixin,
                      PermissionRequiredMixin, UpdateView):
    """Update order in database using order form."""
    model = Order
    form_class = OrderForm
    template_name = 'order_form.html'
    login_url = 'users:user-login'
    permission_required = ('orders.change_order', )
    success_url = reverse_lazy('orders:orders-list')
    success_message = VIEW_MSG['order']['update_success']

    def form_invalid(self, form):
        add_error_messages(request=self.request, forms=[form, ],
                           base_msg=VIEW_MSG['order']['update_error'])
        return super().form_invalid(form)


class OrderDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Delete order with measurement report from database."""
    model = Order
    template_name = 'order_confirm_delete.html'
    login_url = 'users:user-login'
    permission_required = ('orders.delete_order', )
    success_url = reverse_lazy('orders:orders-list')
    success_message = VIEW_MSG['order']['delete_success']

    def delete(self, request, *args, **kwargs):
        messages.success(request, self.success_message)
        return super().delete(request, *args, **kwargs)


class MeasurementReportCreateView(SuccessMessageMixin, LoginRequiredMixin,
                                  PermissionRequiredMixin, CreateView):
    """Create a new measurement report with measurements in database
    using measurement report form & measurements formset.
    """
    form_class = MeasurementReportForm
    template_name = 'measurement_report_form.html'
    login_url = 'users:user-login'
    permission_required = ('orders.add_measurementreport', )
    success_url = reverse_lazy('orders:orders-list')
    success_message = VIEW_MSG['measurement_report']['new_success']

    def get_context_data(self, **kwargs):
        """Add to context formset & order reference for measurement report."""
        context = super().get_context_data(**kwargs)
        context['formset'] = MeasurementFormSet()
        context['order'] = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        return context

    def post(self, request, *args, **kwargs):
        """Pack measurement report form and measurements formset into
        measurement report multiform.
        """
        multiform = {'form': self.get_form(), 'formset': MeasurementFormSet(data=request.POST)}
        if all(form.is_valid() for form in multiform.values()):
            return self.form_valid(multiform)
        else:
            return self.form_invalid(multiform)

    def form_valid(self, multiform):
        """Retrieve order object, set its status as open, and
        set as reference for created measurement report with measurements.
        """
        order = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        order.status = 'Open'
        order.save()

        measurement_report = multiform['form'].save(commit=False)
        measurement_report.order = order
        measurement_report.save()

        for measurement_form in multiform['formset']:
            measurement = measurement_form.save(commit=False)
            measurement.measurement_report = measurement_report
            measurement.save()

        messages.success(self.request, self.success_message)
        return redirect(self.success_url)

    def form_invalid(self, multiform):
        add_error_messages(request=self.request,
                           forms=[multiform['form'], [form for form in multiform['formset']]],
                           base_msg=VIEW_MSG['measurement_report']['new_error'])
        return super().form_invalid(multiform['form'])


class MeasurementReportDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Provide information about order with referenced
    measurement report and its measurements.
    """
    model = Order
    template_name = 'measurement_report_detail.html'
    login_url = 'users:user-login'
    permission_required = ('orders.view_measurementreport', )


class MeasurementReportUpdateView(SuccessMessageMixin, LoginRequiredMixin,
                                  PermissionRequiredMixin, UpdateView):
    """Update measurement report with measurements in database using
    measurement report form & measurements formset.
    """
    model = Order
    form_class = MeasurementReportForm
    template_name = 'measurement_report_form.html'
    login_url = 'users:user-login'
    permission_required = ('orders.change_measurementreport', )
    success_url = reverse_lazy('orders:orders-list')
    success_message = VIEW_MSG['measurement_report']['update_success']

    def dispatch(self, request, *args, **kwargs):
        self.object = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Add to context formset & order reference for measurement report.
        Bind to form order referenced measurement report instance."""
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(instance=self.object.measurement_report)
        context['formset'] = MeasurementFormSet(instance=self.object.measurement_report,
                                                queryset=self.object.measurement_report.measurements.all())
        context['order'] = self.object
        return context

    def get(self, request, *args, **kwargs):
        """Check if measurement report of closed order is not served."""
        if self.object.status == 'Done':
            messages.error(request, message=VIEW_MSG['orders']['measurement_report'])
            return redirect('orders:orders-list')
        else:
            return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Pack measurement report form and measurements formset into
        measurement report multiform.
        """
        form = MeasurementReportForm(data=request.POST, instance=self.object.measurement_report)
        formset = MeasurementFormSet(data=request.POST, instance=self.object.measurement_report)
        multiform = {'form': form, 'formset': formset}
        if all(form.is_valid() for form in multiform.values()):
            return self.form_valid(multiform)
        else:
            return self.form_invalid(multiform)

    def form_valid(self, multiform):
        """Update measurements in database for measurements formset.
        Remove all extra measurements if are not present in formset.
        """
        measurement_report = multiform['form'].save()

        measurements = []
        for form in multiform['formset']:
            measurement = form.save(commit=False)
            measurement.instance = measurement_report
            measurements.append(measurement)
            measurement.save()
        for measurement in measurement_report.measurements.all():
            if measurement not in measurements:
                measurement.delete()

        messages.success(self.request, self.success_message)
        return redirect(self.success_url)

    def form_invalid(self, multiform):
        add_error_messages(request=self.request, forms=[multiform['form'],
                                                        [form for form in multiform['formset']]],
                           base_msg=VIEW_MSG['measurement_report']['update_error'])
        return super().form_invalid(multiform['form'])


class MeasurementReportCloseView(SuccessMessageMixin, LoginRequiredMixin,
                                 PermissionRequiredMixin, FormView):
    """Close measurement report & measurements."""
    model = Order
    form_class = OrderForm
    template_name = 'measurement_confirm_close.html'
    login_url = 'users:user-login'
    permission_required = ('orders.delete_measurementreport', )
    success_url = reverse_lazy('orders:orders-list')
    success_message = VIEW_MSG['measurement_report']['close_success']

    def get(self, request, *args, **kwargs):
        """Check if closing measurement report view is called properly."""
        order = get_object_or_404(self.model, pk=self.kwargs.get('pk'))
        try:
            order.measurement_report
        except MeasurementReport.DoesNotExist:
            messages.error(request, message=VIEW_MSG['measurement_report']['close_not_saved_error'])
            return redirect('orders:orders-list')
        if order.status == 'Done':
            messages.error(request, message=VIEW_MSG['measurement_report']['close_access_error'])
            return redirect('orders:orders-list')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Closing measurement report is performed as set order status as done."""
        order = get_object_or_404(self.model, pk=self.kwargs.get('pk'))
        order.status = 'Done'
        order.save()
        messages.success(request, message=self.success_message)
        return redirect('orders:orders-list')
