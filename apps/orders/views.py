from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView, FormView

from apps.constants import PAGINATION_OBJ_COUNT_PER_PAGE, VIEW_MSG
from .filters import OrderFilter

from .forms import OrderForm, MeasurementFormSet, MeasurementReportForm, DateFilteringForm
from .models import Order, MeasurementReport
from apps.view_helpers import add_error_messages


class OrderListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Order
    template_name = 'orders_list.html'
    login_url = 'users:user-login'
    permission_required = ('orders.view_order', )
    paginate_by = PAGINATION_OBJ_COUNT_PER_PAGE
    ordering = ('id', )

    def get_queryset(self):
        for param in self.request.GET:
            param_val = self.request.GET.get(param)
            if param_val is not None:
                self.request.session[param] = param_val
        if 'clear_filters' in self.request.GET:
            for field_name in OrderFilter.get_fields():
                self.request.session[field_name] = ''
            self.request.session['date_of_production_after'] = Order.get_date_of_production('today')
            self.request.session['date_of_production_before'] = Order.get_date_of_production('max')

        order_filter = OrderFilter(self.request.session, queryset=self.model.objects.all())
        qs = order_filter.qs.order_by(self.get_ordering())
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date_filtering_form = DateFilteringForm(initial={
            'date_of_production_after': self.request.session.get('date_of_production_after'),
            'date_of_production_before': self.request.session.get('date_of_production_before'), })
        context['date_filtering_form'] = date_filtering_form
        return context

    def get_ordering(self):
        ordering = self.request.GET.get('ordering')
        if ordering is not None:
            self.request.session['ordering'] = ordering
        if 'clear_filters' in self.request.GET:
            self.request.session['ordering'] = 'id'
        return self.request.session.get('ordering', 'id')


class OrderCreateView(SuccessMessageMixin, LoginRequiredMixin,
                      PermissionRequiredMixin, CreateView):
    form_class = OrderForm
    template_name = 'order_form.html'
    login_url = 'users:user-login'
    permission_required = ('orders.add_order', )
    success_url = reverse_lazy('orders:orders-list')
    success_message = VIEW_MSG['order']['new_success']

    def form_invalid(self, form):
        add_error_messages(self.request, VIEW_MSG['order']['new_error'], form)
        return super().form_invalid(form)


class OrderDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Order
    template_name = 'order_detail.html'
    login_url = 'users:user-login'
    permission_required = ('orders.view_order', )


class OrderUpdateView(SuccessMessageMixin, LoginRequiredMixin,
                      PermissionRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'order_form.html'
    login_url = 'users:user-login'
    permission_required = ('orders.change_order', )
    success_url = reverse_lazy('orders:orders-list')
    success_message = VIEW_MSG['order']['update_success']

    def form_invalid(self, form):
        add_error_messages(self.request, VIEW_MSG['order']['update_error'], form)
        return super().form_invalid(form)


class OrderDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
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
    form_class = MeasurementReportForm
    template_name = 'measurement_report_form.html'
    login_url = 'users:user-login'
    permission_required = ('orders.add_measurementreport', )
    success_url = reverse_lazy('orders:orders-list')
    success_message = VIEW_MSG['measurement_report']['new_success']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = MeasurementFormSet()
        context['order'] = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        return context

    def post(self, request, *args, **kwargs):
        multiform = {'form': self.get_form(), 'formset': MeasurementFormSet(data=request.POST)}
        if all(form.is_valid() for form in multiform.values()):
            return self.form_valid(multiform)
        else:
            return self.form_invalid(multiform)

    def form_valid(self, multiform):
        order = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        measurement_report = multiform['form'].save(commit=False)
        measurement_report.order = order
        measurement_report.save()

        order.status = 'Open'
        order.save()

        for measurement_form in multiform['formset']:
            measurement = measurement_form.save(commit=False)
            measurement.measurement_report = measurement_report
            measurement.save()

        messages.success(self.request, self.success_message)
        return redirect(self.success_url)

    def form_invalid(self, multiform):
        add_error_messages(self.request, VIEW_MSG['measurement_report']['new_error'], multiform)
        return super().form_invalid(multiform['form'])


class MeasurementReportDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Order
    template_name = 'measurement_report_detail.html'
    login_url = 'users:user-login'
    permission_required = ('orders.view_measurementreport', )


class MeasurementReportUpdateView(SuccessMessageMixin, LoginRequiredMixin,
                                  PermissionRequiredMixin, UpdateView):
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
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(instance=self.object.measurement_report)
        context['formset'] = MeasurementFormSet(instance=self.object.measurement_report,
                                                queryset=self.object.measurement_report.measurements.all())
        context['order'] = self.object
        return context

    def get(self, request, *args, **kwargs):
        if self.object.status == 'Done':
            messages.error(request, message="Zamknięte raporty pomiarowe nie podlegają edycji")
            return redirect('orders:orders-list')
        else:
            return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = MeasurementReportForm(data=request.POST, instance=self.object.measurement_report)
        formset = MeasurementFormSet(data=request.POST, instance=self.object.measurement_report)
        multiform = {'form': form, 'formset': formset}
        if all(form.is_valid() for form in multiform.values()):
            return self.form_valid(multiform)
        else:
            return self.form_invalid(multiform)

    def form_valid(self, multiform):
        measurement_report = multiform['form'].save(commit=False)
        measurement_report.order = self.object
        measurement_report.save()

        # this solution is caused by invalid management form in formset in template
        # formset can automatically delete unused forms, but such form must be marked in management form
        # for deletion: delete field must be set for on : DELETE: on
        # Proposed solution: integrate django-dynamic-formset in templates - replace current frontend mechanism
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
        add_error_messages(self.request, VIEW_MSG['measurement_report']['update_error'], form=multiform['form'],
                           secondary_forms=[form for form in multiform['formset']])
        return super().form_invalid(multiform['form'])


class MeasurementReportCloseView(SuccessMessageMixin, LoginRequiredMixin,
                                 PermissionRequiredMixin, FormView):
    model = Order
    form_class = OrderForm
    template_name = 'measurement_confirm_close.html'
    login_url = 'users:user-login'
    permission_required = ('orders.delete_measurementreport', )
    success_url = reverse_lazy('orders:orders-list')
    success_message = VIEW_MSG['measurement_report']['close_success']

    def get(self, request, *args, **kwargs):
        order = get_object_or_404(self.model, pk=self.kwargs.get('pk'))
        try:
            order.measurement_report
        except MeasurementReport.DoesNotExist:
            messages.error(request, message="Nie można zamknąć raportu pomiarowego, który nie został zapisany.")
            return redirect('orders:orders-list')
        if order.status == 'Done':
            messages.error(request, message="Raport pomiarowy już został zamknięty.")
            return redirect('orders:orders-list')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(self.model, pk=self.kwargs.get('pk'))
        order.status = 'Done'
        order.save()
        messages.success(request, message=self.success_message)
        return redirect('orders:orders-list')
