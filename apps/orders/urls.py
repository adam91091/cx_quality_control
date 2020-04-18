from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.orders_list, name='orders_list'),
    path('new/', views.order_new, name='order_new'),
    path('update/<int:order_id>', views.order_update, name='order_update'),
    path('delete/<int:order_id>', views.order_delete, name='order_delete'),
]
