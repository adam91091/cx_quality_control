from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate

from apps.users.forms import CxUserLoginForm
from apps.views_utils import VIEW_MSG


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
    return render(request, 'login_form.html', {'login_form': login_form})


def user_logout(request):
    if request.user.is_active:
        logout(request=request)
        messages.success(request, message=VIEW_MSG['user']['logout_success'])
    return redirect(to='users:user_login')
