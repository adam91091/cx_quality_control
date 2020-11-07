from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetConfirmView, PasswordChangeView
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.decorators import login_required

from apps.users.forms import CxUserLoginForm, CxUserPasswordResetForm, CxUserEmailChangeForm, CxUserPasswordChangeForm
from apps.users.models import CxUser
from apps.views_utils import VIEW_MSG, add_error_messages


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request=request, user=user)
                messages.success(request, message=VIEW_MSG['user']['login_success'])
                return redirect(to='clients:clients_list')
            else:
                messages.error(request, message=VIEW_MSG['user']['inactive'])
        else:
            messages.error(request, message=VIEW_MSG['user']['login_fail'])

    login_form = CxUserLoginForm()
    return render(request, 'login_form.html', {'form': login_form})


def user_logout(request):
    if request.user.is_active:
        logout(request=request)
        messages.success(request, message=VIEW_MSG['user']['logout_success'])
    return redirect(to='users:user_login')


@login_required
def user_profile(request):
    return render(request, 'profile_form.html')


@login_required
def user_email_change(request):
    if request.method == 'POST':
        form = CxUserEmailChangeForm(instance=request.user, data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, VIEW_MSG['user']['email_change_success'])
            return redirect(to='users:user_profile')
        else:
            add_error_messages(request, main_msg=VIEW_MSG['user']['email_change_error'],
                               form=form)
    form = CxUserEmailChangeForm(instance=request.user)
    return render(request, 'email_change_form.html', {'form': form})


def user_reset_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = CxUser.objects.get(username=username)
            if user:
                if user.is_active:
                    subject = "Password Reset Request"
                    email_template_name = "password_reset_email.txt"
                    c = {
                        "email": user.email,
                        "domain": "127.0.0.1:8000",
                        "site_name": "Cx-quality-control",
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        "token": default_token_generator.make_token(user=user),
                        "protocol": "http",
                    }
                    email_msg = render_to_string(template_name=email_template_name, context=c)
                    try:
                        send_mail(subject=subject, message=email_msg, from_email="admin@example.com",
                                  recipient_list=[user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse("Invalid header found")
                    return redirect(to='users:password_reset_done', user_id=user.id)
                else:
                    messages.error(request, message=VIEW_MSG['user']['inactive'])
        except CxUser.DoesNotExist:
            messages.error(request, message="Użytkownik o podanym loginie nie istnieje w bazie danych")
    user_form = CxUserLoginForm()
    return render(request, 'password_reset_form.html', {'user_form': user_form})


def user_password_reset_done(request, user_id):
    try:
        user = CxUser.objects.get(id=user_id)
        domain = user.email.split('@')[1]
    except (CxUser.DoesNotExist, IndexError):
        domain = 'nieprawidłowy format adresu email'
    return render(request, 'password_reset_done.html', {'domain': domain})


class CxUserPasswordChangeView(PasswordChangeView):
    form_class = CxUserPasswordChangeForm
    success_url = reverse_lazy('users:user_profile')

    def post(self, request, **kwargs):
        form = self.get_form()
        if form.is_valid():
            messages.success(request=request, message=VIEW_MSG['user']['password_change_success'])
            return self.form_valid(form)
        else:
            add_error_messages(request=request, main_msg=VIEW_MSG['user']['password_change_fail'], form=form)
            return self.form_invalid(form)


class CxUserPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CxUserPasswordResetForm
    success_url = reverse_lazy('users:password_reset_complete')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, **kwargs):
        form = self.get_form()
        if form.is_valid():
            messages.success(request=request, message=VIEW_MSG['user']['password_change_success'])
            return self.form_valid(form)
        else:
            add_error_messages(request=request, main_msg=VIEW_MSG['user']['password_change_fail'], form=form)
            return self.form_invalid(form)
