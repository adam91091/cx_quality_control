from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import OrderForm, MeasurementFormSet, MeasurementReportForm
from .models import Order
from ..clients.models import Client
from ..products.models import Product
from ..views_utils import render_form_response, VIEW_MSG, check_if_related_object_exists, add_error_messages


def orders_list(request):
    orders = Order.objects.all()
    return render(request, 'orders_list.html', {'orders': orders})


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
    if request.method == 'POST':
        order_form = OrderForm(data=request.POST, instance=order)
        measurement_report_form = MeasurementReportForm(data=request.POST)
        measurement_formset = MeasurementFormSet(data=request.POST)
    else:
        order_form = OrderForm(instance=order, measurement_report=True)
        measurement_report_form = MeasurementReportForm()
        measurement_formset = MeasurementFormSet()
    return _render_measurement_form_response(request=request, order_form=order_form,
                                             measurement_report_form=measurement_report_form,
                                             measurement_formset=measurement_formset, method='new')


def measurement_report_update(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        order_form = OrderForm(data=request.POST, instance=order)
        measurement_report_form = MeasurementReportForm(data=request.POST, instance=order.measurement_report)
        measurement_formset = MeasurementFormSet(data=request.POST, instance=order.measurement_report,
                                                 queryset=order.measurement_report.measurements.all())
    else:
        order_form = OrderForm(instance=order, measurement_report=True)
        measurement_report_form = MeasurementReportForm(instance=order.measurement_report)
        measurement_formset = MeasurementFormSet(instance=order.measurement_report,
                                                 queryset=order.measurement_report.measurements.all())
    return _render_measurement_form_response(request=request, order_form=order_form,
                                             measurement_report_form=measurement_report_form,
                                             measurement_formset=measurement_formset, method='update')


def _render_measurement_form_response(request, order_form, measurement_report_form, measurement_formset, method):
    if order_form.is_valid() and measurement_report_form.is_valid():
        if all(measurement_form.is_valid() for measurement_form in measurement_formset):
            order = order_form.save(commit=False)
            order.save()
            measurement_report = measurement_report_form.save(commit=False)
            measurement_report.order = order
            measurement_report.save()
            for measurement_form in measurement_formset:
                measurement = measurement_form.save(commit=False)
                measurement.measurement_report = measurement_report
                measurement.save()
            if method == 'new':
                order.status = 'Open'
                order.save()
            messages.success(request, VIEW_MSG['measurement_report'][f'{method}_success'])
            return redirect('orders:orders_list')
    if request.method == 'POST':
        add_error_messages(request, main_msg=VIEW_MSG['measurement_report'][f'{method}_error'], form=order_form,
                           secondary_forms=[measurement_report_form] + [_ for _ in measurement_formset])

    return render(request, 'measurement_report_form.html', {'order_form': order_form,
                                                            'measurement_report_form': measurement_report_form,
                                                            'measurement_formset': measurement_formset})
