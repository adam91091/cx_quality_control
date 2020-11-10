from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required, login_required
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, DetailView, DeleteView

from apps.products.forms import ProductForm, SpecificationForm, ProductSpecificationMultiForm
from apps.products.models import Product
from apps.providers import FilterProvider, PaginationProvider, SortingProvider
from apps.views_utils import VIEW_MSG, add_error_messages


@login_required
@permission_required('products.view_product')
def products_list(request):
    product_filter_provider = FilterProvider(model=Product, session=request.session, params=request.GET)
    products = product_filter_provider.get_queryset()
    product_sorting_provider = SortingProvider(model=Product, session=request.session, params=request.GET)
    products = product_sorting_provider.sort_queryset(queryset=products)
    order_by = product_sorting_provider.get_next_order_by()

    product_pagination_provider = PaginationProvider(queryset=products, page=request.GET.get('page', 1))
    page_obj, pages_range = product_pagination_provider.paginate()

    return render(request, 'products_list.html', {'page_obj': page_obj,
                                                  'pages_range': pages_range,
                                                  'order_by': order_by})


class ProductCreateView(SuccessMessageMixin, LoginRequiredMixin,
                        PermissionRequiredMixin, CreateView):
    form_class = ProductSpecificationMultiForm
    template_name = 'product_form.html'
    login_url = 'users:user_login'
    permission_required = ('products.add_product', )
    success_url = reverse_lazy('products:products_list')
    success_message = VIEW_MSG['product']['new_success']

    def form_valid(self, form):
        product = form['product'].save()
        specification = form['spec'].save(commit=False)
        specification.product = product
        specification.save()
        messages.success(self.request, self.success_message)
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_validation_hints'] = ProductForm.validation_hints
        context['spec_validation_hints'] = SpecificationForm.validation_hints
        return context

    def form_invalid(self, form):
        add_error_messages(self.request, VIEW_MSG['product']['update_error'], form)
        return super().form_invalid(form)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    login_url = 'users:user_login'
    permission_required = ('products.view_product', )


class ProductUpdateView(SuccessMessageMixin, LoginRequiredMixin,
                        PermissionRequiredMixin, UpdateView):
    form_class = ProductSpecificationMultiForm
    model = Product
    template_name = 'product_form.html'
    login_url = 'users:user_login'
    permission_required = ('products.change_product', )
    success_url = reverse_lazy('products:products_list')
    success_message = VIEW_MSG['product']['update_success']

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(instance={
            'product': self.object,
            'spec': self.object.specification
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_validation_hints'] = ProductForm.validation_hints
        context['spec_validation_hints'] = SpecificationForm.validation_hints
        return context

    def form_invalid(self, form):
        add_error_messages(self.request, VIEW_MSG['product']['update_error'], form)
        return super().form_invalid(form)


class ProductDeleteView(SuccessMessageMixin, LoginRequiredMixin,
                        PermissionRequiredMixin, DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    login_url = 'users:user_login'
    permission_required = 'products.delete_product'
    success_url = reverse_lazy('products:products_list')
    success_message = VIEW_MSG['product']['delete_success']

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
