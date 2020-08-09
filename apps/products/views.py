from django.contrib import messages
from django.shortcuts import render, redirect

from apps.products.forms import ProductForm, SpecificationForm
from apps.products.models import Product
from apps.providers import ListViewFilterProvider
from apps.views_utils import VIEW_MSG, render_one_to_one_form_response


def products_list(request):
    # products = Product.objects.all()
    # return render(request, 'products_list.html', {'products': products})
    product_provider = ListViewFilterProvider(request=request, model=Product, fields=('product_sap_id', 'index',
                                                                                      'description'))
    request = product_provider.run()
    return render(request, 'products_list.html', {'page_obj': product_provider.page_obj,
                                                  'pages_range': product_provider.pages_range,
                                                  'order_by': product_provider.get_order_by_switch()})


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    product_form = ProductForm(instance=product, read_only=True)
    spec_form = SpecificationForm(instance=product.specification, read_only=True)
    return render(request, 'product_form.html', {'product_form': product_form, 'spec_form': spec_form,
                                                 'type': 'detail'})


def product_delete(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        product.specification.delete()
        product.delete()
        messages.success(request, VIEW_MSG['product']['delete'])
        return redirect('products:products_list')
    else:
        return render(request, 'product_confirm_delete.html', {'product': product})


def product_new(request):
    if request.method == 'POST':
        product_form = ProductForm(data=request.POST)
        spec_form = SpecificationForm(data=request.POST)
    else:
        product_form = ProductForm()
        spec_form = SpecificationForm()
    return render_one_to_one_form_response(request=request, method='new', parent_form=product_form,
                                           child_form=spec_form, parent_name='product', child_name='spec')


def product_update(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        product_form = ProductForm(data=request.POST, instance=product)
        spec_form = SpecificationForm(data=request.POST, instance=product.specification)
    else:
        product_form = ProductForm(instance=product)
        spec_form = SpecificationForm(instance=product.specification)
    return render_one_to_one_form_response(request=request, method='update', parent_form=product_form,
                                           child_form=spec_form, parent_name='product', child_name='spec')
