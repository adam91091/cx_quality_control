from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required, login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView

from apps.globals import PAGINATION_OBJ_COUNT_PER_PAGE
from .filters import OrderFilter

from .forms import OrderForm, MeasurementFormSet, MeasurementReportForm, DateFilteringForm, MeasurementForm
from .models import Order, MeasurementReport
from ..views_utils import VIEW_MSG, add_error_messages


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


@login_required
@permission_required("orders.add_measurementreport")
def measurement_report_new(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'GET':
        order_form = OrderForm(instance=order, measurement_report=True)
        measurement_report_form = MeasurementReportForm()
        measurement_formset = MeasurementFormSet()
        return render(request, 'measurement_report_form.html', {'order_form': order_form,
                                                                'measurement_report_form': measurement_report_form,
                                                                'measurement_formset': measurement_formset,
                                                                'order_id': order_id, 'type': 'new'})
    else:
        order_form = OrderForm(data=request.POST, instance=order)
        measurement_report_form = MeasurementReportForm(data=request.POST)
        measurement_formset = MeasurementFormSet(data=request.POST)
        if not check_report_data(data=request.POST):
            messages.error(request, 'Numery zmierzonych palet nie mogą się powtarzać!')
            return render(request, 'measurement_report_form.html', {'order_form': order_form,
                                                                    'measurement_report_form': measurement_report_form,
                                                                    'measurement_formset': measurement_formset,
                                                                    'order_id': order_id, 'type': 'new'})
        return _render_measurement_form_post(request=request, order_form=order_form,
                                             measurement_report_form=measurement_report_form,
                                             measurement_formset=measurement_formset, method='new', order_id=order_id)


@login_required
@permission_required("orders.view_measurementreport")
def measurement_report_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    order_form = OrderForm(instance=order, read_only=True)
    measurement_report_form = MeasurementReportForm(instance=order.measurement_report, read_only=True)
    measurement_formset = MeasurementFormSet(instance=order.measurement_report,
                                             queryset=order.measurement_report.measurements.all())
    for form in measurement_formset.forms:
        MeasurementForm.make_form_readonly(form)
    return render(request, 'measurement_report_form.html', {'order_form': order_form,
                                                            'measurement_report_form': measurement_report_form,
                                                            'measurement_formset': measurement_formset,
                                                            'order_id': order_id, 'type': 'detail'})


@login_required
@permission_required("orders.change_measurementreport")
def measurement_report_update(request, order_id):
    order = Order.objects.get(id=order_id)
    if order.status == 'Done':
        messages.error(request, message="Zamknięte raporty pomiarowe nie podlegają edycji")
        return redirect('orders:orders-list')
    if request.method == 'GET':
        order_form = OrderForm(instance=order, measurement_report=True)
        measurement_report_form = MeasurementReportForm(instance=order.measurement_report)
        measurement_formset = MeasurementFormSet(instance=order.measurement_report,
                                                 queryset=order.measurement_report.measurements.all())
        return render(request, 'measurement_report_form.html', {'order_form': order_form,
                                                                'measurement_report_form': measurement_report_form,
                                                                'measurement_formset': measurement_formset,
                                                                'order_id': order_id, 'type': 'update'})
    else:
        order_form = OrderForm(data=request.POST, instance=order)
        measurement_ids = [request.POST[key] for key in request.POST.keys() if 'measurements-' in key and '-id' in key]
        measurement_report_form = MeasurementReportForm(data=request.POST, instance=order.measurement_report)
        queryset = order.measurement_report.measurements.filter(id__in=measurement_ids)
        measurement_formset = MeasurementFormSet(data=request.POST, instance=order.measurement_report,
                                                 queryset=queryset)
        if not check_report_data(data=request.POST):
            messages.error(request, 'Numery zmierzonych palet nie mogą się powtarzać!')
            return render(request, 'measurement_report_form.html', {'order_form': order_form,
                                                                    'measurement_report_form': measurement_report_form,
                                                                    'measurement_formset': measurement_formset,
                                                                    'order_id': order_id, 'type': 'new'})
        return _render_measurement_form_post(request=request, order_form=order_form,
                                             measurement_report_form=measurement_report_form,
                                             measurement_formset=measurement_formset, method='update',
                                             order_id=order_id)


@login_required
@permission_required("orders.delete_measurementreport")
def measurement_report_close(request, order_id):
    order = Order.objects.get(id=order_id)
    try:
        order.measurement_report
    except MeasurementReport.DoesNotExist:
        messages.error(request, message="Nie można zamknąć raportu pomiarowego, który nie został zapisany.")
        return redirect('orders:orders-list')
    if order.status == 'Done':
        messages.error(request, message="Raport pomiarowy już został zamknięty.")
        return redirect('orders:orders-list')
    if request.method == 'POST':
        order.status = 'Done'
        order.save()
        messages.success(request, VIEW_MSG['measurement_report']['close_success'])
        return redirect('orders:orders-list')
    else:
        return render(request, 'measurement_confirm_close.html', {'order': order})


def _render_measurement_form_post(request, order_form, measurement_report_form, measurement_formset, method,
                                  order_id):
    if order_form.is_valid() and measurement_report_form.is_valid():
        if all(measurement_form.is_valid() for measurement_form in measurement_formset):
            order = order_form.save(commit=False)
            measurement_report = measurement_report_form.save(commit=False)
            measurement_report.order = order
            measurement_report.save()
            measurements = []
            for measurement_form in measurement_formset:
                measurement = measurement_form.save(commit=False)
                measurements.append(measurement)
                measurement.measurement_report = measurement_report
                measurement.save()
            if method == 'update':
                for measurement in measurement_report.measurements.all():
                    if measurement not in measurements:
                        measurement.delete()
            if method == 'new':
                order.status = 'Open'
                order.save()
            messages.success(request, VIEW_MSG['measurement_report'][f'{method}_success'])
            return redirect('orders:orders-list')

        add_error_messages(request, main_msg=VIEW_MSG['measurement_report'][f'{method}_error'], form=order_form,
                           secondary_forms=[measurement_report_form] + [_ for _ in measurement_formset])
    return render(request, 'measurement_report_form.html', {'order_form': order_form,
                                                            'measurement_report_form': measurement_report_form,
                                                            'measurement_formset': measurement_formset,
                                                            'order_id': order_id, 'type': method})


def check_report_data(data) -> bool:
    """Check pallet numbers uniqueness"""
    pallet_nums = []
    for key in data:
        if 'pallet_number' in key:
            pallet_nums.append(data[key])
    return len(set(pallet_nums)) == len(pallet_nums)
