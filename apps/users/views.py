from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from apps.users.forms import CxUserPasswordChangeForm, CxUserAuthenticationForm
from apps.views_utils import VIEW_MSG, add_error_messages


class CxUserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'login_form.html'
    form_class = CxUserAuthenticationForm
    success_message = VIEW_MSG['user']['login_success']

    def form_invalid(self, form):
        add_error_messages(self.request, main_msg=VIEW_MSG['user']['login_fail'], form=form)
        return super().form_invalid(form)


class CxUserLogoutView(LoginRequiredMixin, LogoutView):

    def get(self, request, *args, **kwargs):
        messages.success(request, message=VIEW_MSG['user']['logout_success'])
        return redirect('users:user-login')


class CxUserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile_form.html'


class CxUserPasswordChangeView(PasswordChangeView):
    template_name = 'password_change_form.html'
    form_class = CxUserPasswordChangeForm
    success_url = reverse_lazy('users:user-profile')

    def post(self, request, **kwargs):
        form = self.get_form()
        if form.is_valid():
            messages.success(request=request, message=VIEW_MSG['user']['password_change_success'])
            return self.form_valid(form)
        else:
            add_error_messages(request=request, main_msg=VIEW_MSG['user']['password_change_fail'], form=form)
            return self.form_invalid(form)
