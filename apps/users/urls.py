from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('password_reset/', views.user_reset_password, name='password_reset'),
    path('password_reset_done/<int:user_id>/', views.user_password_reset_done, name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', views.CxUserPasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'), name='password_reset_complete'),
]
