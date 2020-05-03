from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import OrderForm, MeasurementFormSet, MeasurementReportForm
from .models import Order
from ..clients.models import Client
from ..products.models import Product
from ..views_utils import render_form_response, VIEW_MSG, check_if_related_object_exists


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
        pass
    else:
        measurement_report_form = MeasurementReportForm()
        measurement_formset = MeasurementFormSet()
        return render(request, 'measurement_report_form.html', {'measurement_formset': measurement_formset,
                                                                'measurement_report_form': measurement_report_form})
