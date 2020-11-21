from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from apps.users.forms import CxUserPasswordChangeForm, CxUserAuthenticationForm
from apps.view_helpers import add_error_messages
from apps.user_texts import VIEW_MSG


class CxUserLoginView(SuccessMessageMixin, LoginView):
    """Login home page view."""
    template_name = 'login_form.html'
    form_class = CxUserAuthenticationForm
    success_message = VIEW_MSG['user']['login_success']

    def form_invalid(self, form):
        add_error_messages(request=self.request, forms=[form, ],
                           base_msg=VIEW_MSG['user']['login_fail'])
        return super().form_invalid(form)


class CxUserLogoutView(LoginRequiredMixin, LogoutView):
    """Redirect to login home page after logout."""
    def get(self, request, *args, **kwargs):
        messages.success(request, message=VIEW_MSG['user']['logout_success'])
        return redirect('users:user-login')


class CxUserProfileView(LoginRequiredMixin, TemplateView):
    """Display user profile data."""
    template_name = 'profile_detail.html'


class CxUserPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    """Allows user password change."""
    template_name = 'password_change_form.html'
    form_class = CxUserPasswordChangeForm
    success_url = reverse_lazy('users:user-profile')
    success_message = VIEW_MSG['user']['password_change_success']

    def form_invalid(self, form):
        add_error_messages(request=self.request, forms=[form, ],
                           base_msg=VIEW_MSG['user']['password_change_fail'])
        return super().form_invalid(form)
