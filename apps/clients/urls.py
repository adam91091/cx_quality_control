from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path('', views.clients_list, name='clients_list'),
    path('new/', views.client_new, name='client_new'),
    path('detail/<int:client_id>', views.client_detail, name='client_detail'),
    path('update/<int:client_id>', views.client_update, name='client_update'),
    path('delete/<int:client_id>', views.client_delete, name='client_delete'),
]
