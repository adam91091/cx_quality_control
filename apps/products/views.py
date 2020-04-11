from django.contrib import messages
from django.shortcuts import render, redirect

from apps.products.forms import ProductForm, SpecificationForm
from apps.products.models import Product
from apps.views_utils import VIEW_MSG, add_error_messages


def products_list(request):
    products = Product.objects.all()
    return render(request, 'products_list.html', {'products': products})


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    product_form = ProductForm(instance=product, read_only=True)
    spec_form = SpecificationForm(instance=product.specification, read_only=True)
    return render(request, 'product_form.html', {'product_form': product_form, 'spec_form': spec_form,
                                                 'type': 'detail'})


def product_new(request):
    if request.method == 'POST':
        product_form = ProductForm(data=request.POST)
        spec_form = SpecificationForm(data=request.POST)
        if product_form.is_valid() and spec_form.is_valid():
            product = product_form.save(commit=False)
            product.save()
            messages.success(request, VIEW_MSG['product']['new_success'])
            specification = spec_form.save(commit=False)
            specification.product = product
            specification.save()
            return redirect('products:products_list')
        else:
            add_error_messages(request, main_msg=VIEW_MSG['product']['new_error'],
                               form=product_form, secondary_forms=[spec_form, ])
            return render(request, 'product_form.html', {'product_form': product_form, 'spec_form': spec_form,
                                                         'type': 'new'})
    else:
        product_form = ProductForm()
        spec_form = SpecificationForm()
        return render(request, 'product_form.html', {'product_form': product_form, 'spec_form': spec_form,
                                                     'type': 'new'})


def product_update(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        product_form = ProductForm(data=request.POST, instance=product)
        spec_form = SpecificationForm(data=request.POST, instance=product.specification)
        if product_form.is_valid() and spec_form.is_valid():
            product = product_form.save(commit=False)
            product.save()
            messages.success(request, VIEW_MSG['product']['update_success'])
            specification = spec_form.save(commit=False)
            specification.product = product
            specification.save()
            return redirect('products:products_list')
        else:
            add_error_messages(request, main_msg=VIEW_MSG['client']['update_error'],
                               form=product_form, secondary_forms=[spec_form, ])
            return render(request, 'product_form.html', {'product_form': product_form, 'spec_form': spec_form,
                                                         'type': 'update'})

    else:
        product_form = ProductForm(instance=product)
        spec_form = SpecificationForm(instance=product.specification)
        return render(request, 'product_form.html', {'product_form': product_form, 'spec_form': spec_form,
                                                     'type': 'update'})


def product_delete(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        product.specification.delete()
        product.delete()
        messages.success(request, VIEW_MSG['product']['delete'])
        return redirect('products:products_list')
    else:
        return render(request, 'product_confirm_delete.html', {'product': product})
