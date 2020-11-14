from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, DetailView, DeleteView, ListView

from apps.products.filters import ProductFilter
from apps.products.forms import ProductForm, SpecificationForm, ProductSpecificationMultiForm
from apps.products.models import Product
from apps.constants import PAGINATION_OBJ_COUNT_PER_PAGE, VIEW_MSG
from apps.view_helpers import add_error_messages


class ProductListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Product
    template_name = 'products_list.html'
    login_url = 'users:user-login'
    permission_required = ('products.view_product', )
    paginate_by = PAGINATION_OBJ_COUNT_PER_PAGE
    ordering = ('id', )

    def get_queryset(self):
        for param in self.request.GET:
            param_val = self.request.GET.get(param)
            if param_val is not None:
                self.request.session[param] = param_val
        if 'clear_filters' in self.request.GET:
            for field_name in ProductFilter.get_fields():
                self.request.session[field_name] = ''

        product_filter = ProductFilter(self.request.session, queryset=self.model.objects.all())
        qs = product_filter.qs.order_by(self.get_ordering())
        return qs

    def get_ordering(self):
        ordering = self.request.GET.get('ordering')
        if ordering is not None:
            self.request.session['ordering'] = ordering
        if 'clear_filters' in self.request.GET:
            self.request.session['ordering'] = 'id'
        return self.request.session.get('ordering', 'id')


class ProductCreateView(SuccessMessageMixin, LoginRequiredMixin,
                        PermissionRequiredMixin, CreateView):
    form_class = ProductSpecificationMultiForm
    template_name = 'product_form.html'
    login_url = 'users:user-login'
    permission_required = ('products.add_product', )
    success_url = reverse_lazy('products:products-list')
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
    login_url = 'users:user-login'
    permission_required = ('products.view_product', )


class ProductUpdateView(SuccessMessageMixin, LoginRequiredMixin,
                        PermissionRequiredMixin, UpdateView):
    form_class = ProductSpecificationMultiForm
    model = Product
    template_name = 'product_form.html'
    login_url = 'users:user-login'
    permission_required = ('products.change_product', )
    success_url = reverse_lazy('products:products-list')
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
    login_url = 'users:user-login'
    permission_required = 'products.delete_product'
    success_url = reverse_lazy('products:products-list')
    success_message = VIEW_MSG['product']['delete_success']

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
