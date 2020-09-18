from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.orders_list, name='orders_list'),
    path('new/', views.order_new, name='order_new'),
    path('update/<int:order_id>', views.order_update, name='order_update'),
    path('delete/<int:order_id>', views.order_delete, name='order_delete'),
    path('detail/<int:order_id>', views.order_detail, name='order_detail'),
    path('measurement_report_new/<int:order_id>', views.measurement_report_new, name='measurement_report_new'),
    path('measurement_report_update/<int:order_id>', views.measurement_report_update, name='measurement_report_update'),
    path('measurement_report_close/<int:order_id>', views.measurement_report_close, name='measurement_report_close'),
]
