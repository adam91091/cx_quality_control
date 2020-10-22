from apps.providers import MAX_DATE, MIN_DATE

from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import OrderForm, MeasurementFormSet, MeasurementReportForm, DateFilteringForm, MeasurementForm
from .models import Order

from ..clients.models import Client
from ..products.models import Product
from ..providers import FilterProvider, SortingProvider, PaginationProvider
from ..views_utils import render_form_response, VIEW_MSG, check_if_related_object_exists, add_error_messages


def orders_list(request):
    order_filter_provider = FilterProvider(model=Order, session=request.session, params=request.GET)
    orders = order_filter_provider.get_queryset()
    order_sorting_provider = SortingProvider(model=Order, session=request.session, params=request.GET)
    orders = order_sorting_provider.sort_queryset(queryset=orders)
    order_by = order_sorting_provider.get_next_order_by()

    order_pagination_provider = PaginationProvider(queryset=orders, page=request.GET.get('page', 1))
    page_obj, pages_range = order_pagination_provider.paginate()

    start_from = request.session.get('start_date', MIN_DATE)
    end_to = request.session.get('end_date', MAX_DATE)
    date_filtering_form = DateFilteringForm(initial={'search_start_date': start_from, 'search_end_date': end_to})

    return render(request, 'orders_list.html', {'page_obj': page_obj,
                                                'pages_range': pages_range,
                                                'order_by': order_by,
                                                'date_filtering_form': date_filtering_form})


def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    order_form = OrderForm(instance=order, read_only=True)
    return render(request, 'order_form.html', {'order_form': order_form, 'type': 'detail'})


def order_new(request):
    if request.method == 'POST':
        product = check_if_related_object_exists(request=request, model=Product, sap_id_name='product_sap_id',
                                                 sap_id_value=request.POST.get('product'), model_name='Produkt')
        client = check_if_related_object_exists(request=request, model=Client, sap_id_name='client_sap_id',
                                                sap_id_value=request.POST.get('client'), model_name='Klient')
        order_form = OrderForm(data=request.POST)
        if None in [product, client]:
            return render(request, 'order_form.html', {'order_form': order_form, 'type': 'new'})
    else:
        order_form = OrderForm()
    return render_form_response(request=request, method='new', form=order_form, model_name='order')


def order_update(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        product = check_if_related_object_exists(request=request, model=Product, sap_id_name='product_sap_id',
                                                 sap_id_value=request.POST.get('product'), model_name='Produkt')
        client = check_if_related_object_exists(request=request, model=Client, sap_id_name='client_sap_id',
                                                sap_id_value=request.POST.get('client'), model_name='Klient')
        order_form = OrderForm(data=request.POST, instance=order)
        if None in [product, client]:
            return render(request, 'order_form.html', {'order_form': order_form, 'type': 'update'})
    else:
        order_form = OrderForm(instance=order)
    return render_form_response(request=request, method='update', form=order_form, model_name='order')


def order_delete(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        order.delete()
        messages.success(request, VIEW_MSG['order']['delete'])
        return redirect('orders:orders_list')
    else:
        return render(request, 'order_confirm_delete.html', {'order': order})


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
        return _render_measurement_form_post(request=request, order_form=order_form,
                                             measurement_report_form=measurement_report_form,
                                             measurement_formset=measurement_formset, method='new', order_id=order_id)


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


def measurement_report_update(request, order_id):
    order = Order.objects.get(id=order_id)
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
        return _render_measurement_form_post(request=request, order_form=order_form,
                                             measurement_report_form=measurement_report_form,
                                             measurement_formset=measurement_formset, method='update',
                                             order_id=order_id)


def measurement_report_close(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        order.status = 'Done'
        order.save()
        messages.success(request, VIEW_MSG['measurement_report']['close_success'])
        return redirect('orders:orders_list')
    else:
        return render(request, 'measurement_confirm_close.html', {'order': order})


def _render_measurement_form_post(request, order_form, measurement_report_form, measurement_formset, method,
                                  order_id):

    if order_form.is_valid() and measurement_report_form.is_valid():
        if all(measurement_form.is_valid() for measurement_form in measurement_formset):
            order = order_form.save(commit=False)
            order.save()
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
            return redirect('orders:orders_list')

        add_error_messages(request, main_msg=VIEW_MSG['measurement_report'][f'{method}_error'], form=order_form,
                           secondary_forms=[measurement_report_form] + [_ for _ in measurement_formset])
    return render(request, 'measurement_report_form.html', {'order_form': order_form,
                                                            'measurement_report_form': measurement_report_form,
                                                            'measurement_formset': measurement_formset,
                                                            'order_id': order_id, 'type': method})
