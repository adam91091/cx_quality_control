from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import OrderForm
from .models import Order
from ..clients.models import Client
from ..products.models import Product
from ..views_utils import render_form_response, check_if_object_exists, VIEW_MSG


def orders_list(request):
    orders = Order.objects.all()
    return render(request, 'orders_list.html', {'orders': orders})


def order_new(request):
    if request.method == 'POST':
        data = request.POST.copy()
        product = check_if_object_exists(request=request, model=Product, identifier_name='product_sap_id',
                                         identifier_value=data['product'], model_name='Kod produktu')
        client = check_if_object_exists(request=request, model=Client, identifier_name='client_sap_id',
                                        identifier_value=data['client'], model_name='Nr sap klienta')
        if None in [product, client]:
            return render(request, 'order_form.html', {'order_form': OrderForm(data=data), 'type': 'new'})

        data['product'] = product.id
        data['client'] = client.id
        order_form = OrderForm(data=data)
    else:
        order_form = OrderForm()
    return render_form_response(request=request, method='new', form=order_form, model_name='order')


def order_update(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        data = request.POST.copy()
        product = check_if_object_exists(request=request, model=Product, identifier_name='product_sap_id',
                                         identifier_value=data['product'], model_name='Kod produktu')
        client = check_if_object_exists(request=request, model=Client, identifier_name='client_sap_id',
                                        identifier_value=data['client'], model_name='Nr sap klienta')
        if None in [product, client]:
            order_form = OrderForm(data=data, instance=order)
            return render(request, 'order_form.html', {'order_form': order_form, 'type': 'update'})

        data['product'] = product.id
        data['client'] = client.id
        order_form = OrderForm(data=data, instance=order)
    else:
        data = {'product': order.product.product_sap_id,
                'client': order.client.client_sap_id,
                'order_sap_id': order.order_sap_id,
                'date_of_production': order.date_of_production,
                'quantity': order.quantity,
                'external_diameter_reference': order.external_diameter_reference,
                'internal_diameter_reference': order.internal_diameter_reference,
                'length': order.length,
                }
        order_form = OrderForm(data=data, instance=order)
    return render_form_response(request=request, method='update', form=order_form, model_name='order')


def order_delete(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        order.delete()
        messages.success(request, VIEW_MSG['order']['delete'])
        return redirect('orders:orders_list')
    else:
        return render(request, 'order_confirm_delete.html', {'order': order})
