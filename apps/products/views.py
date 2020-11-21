from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, DetailView, DeleteView, ListView

from apps.products.filters import ProductFilter
from apps.products.forms import ProductForm, SpecificationForm, ProductSpecificationMultiForm
from apps.products.models import Product
from apps.constants import PAGINATION_OBJ_COUNT_PER_PAGE
from apps.user_texts import VIEW_MSG
from apps.view_helpers import add_error_messages, update_filter_params, update_ordering


class ProductListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """List products, provide product filtering and sorting."""
    model = Product
    template_name = 'products_list.html'
    login_url = 'users:user-login'
    permission_required = ('products.view_product', )
    paginate_by = PAGINATION_OBJ_COUNT_PER_PAGE
    ordering = ('id', )

    def get_queryset(self):
        """Update session for request GET parameters.
        Filter & sort products by parameters values stored in session.
        """
        self.request.session = update_filter_params(params=self.request.GET,
                                                    session=self.request.session,
                                                    filter_class=ProductFilter)
        product_filter = ProductFilter(self.request.session, queryset=self.model.objects.all())
        qs = product_filter.qs.order_by(self.get_ordering())
        return qs

    def get_ordering(self):
        """Update session for ordering parameter from request.
        Return ordering value stored in session or id as a default.
        """
        self.request.session = update_ordering(params=self.request.GET,
                                               session=self.request.session)
        return self.request.session.get('ordering', 'id')


class ProductCreateView(SuccessMessageMixin, LoginRequiredMixin,
                        PermissionRequiredMixin, CreateView):
    """Create a new product with specification in database
    using product & specification multiform.
    """
    form_class = ProductSpecificationMultiForm
    template_name = 'product_form.html'
    login_url = 'users:user-login'
    permission_required = ('products.add_product', )
    success_url = reverse_lazy('products:products-list')
    success_message = VIEW_MSG['product']['new_success']

    def form_valid(self, form):
        """Provide custom logic for specification -> product
        relation purpose.
        """
        product = form['product'].save()
        specification = form['spec'].save(commit=False)
        specification.product = product
        specification.save()
        messages.success(self.request, self.success_message)
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        """Add to context client side form hints."""
        context = super().get_context_data(**kwargs)
        context['product_validation_hints'] = ProductForm.validation_hints
        context['spec_validation_hints'] = SpecificationForm.validation_hints
        return context

    def form_invalid(self, form):
        add_error_messages(request=self.request, forms=[form, ],
                           base_msg=VIEW_MSG['product']['new_error'])
        return super().form_invalid(form)


class ProductDetailView(DetailView):
    """Provide information about product with specification."""
    model = Product
    template_name = 'product_detail.html'
    login_url = 'users:user-login'
    permission_required = ('products.view_product', )


class ProductUpdateView(SuccessMessageMixin, LoginRequiredMixin,
                        PermissionRequiredMixin, UpdateView):
    """Update product with specification in database using
    product & specification multiform.
    """
    form_class = ProductSpecificationMultiForm
    model = Product
    template_name = 'product_form.html'
    login_url = 'users:user-login'
    permission_required = ('products.change_product', )
    success_url = reverse_lazy('products:products-list')
    success_message = VIEW_MSG['product']['update_success']

    def get_form_kwargs(self):
        """Put product and specification updating objects
        into kwargs instantiating form class.
        """
        kwargs = super().get_form_kwargs()
        kwargs.update(instance={
            'product': self.object,
            'spec': self.object.specification
        })
        return kwargs

    def get_context_data(self, **kwargs):
        """Add to context client side form hints."""
        context = super().get_context_data(**kwargs)
        context['product_validation_hints'] = ProductForm.validation_hints
        context['spec_validation_hints'] = SpecificationForm.validation_hints
        return context

    def form_invalid(self, form):
        add_error_messages(request=self.request, forms=[form, ],
                           base_msg=VIEW_MSG['product']['update_error'])
        return super().form_invalid(form)


class ProductDeleteView(SuccessMessageMixin, LoginRequiredMixin,
                        PermissionRequiredMixin, DeleteView):
    """Delete product with specification from database.
    All orders referenced to this product are also deleted.
    """
    model = Product
    template_name = 'product_confirm_delete.html'
    login_url = 'users:user-login'
    permission_required = 'products.delete_product'
    success_url = reverse_lazy('products:products-list')
    success_message = VIEW_MSG['product']['delete_success']

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
