from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.CxUserLoginView.as_view(), name='user-login'),
    path('logout/', views.CxUserLogoutView.as_view(), name='user-logout'),
    path('profile/', views.CxUserProfileView.as_view(), name='user-profile'),
    path('password_change/', views.CxUserPasswordChangeView.as_view(), name='password-change'),
]
