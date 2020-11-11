from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    path('', views.OrderListView.as_view(), name='orders-list'),
    path('new/', views.OrderCreateView.as_view(), name='order-new'),
    path('detail/<int:pk>', views.OrderDetailView.as_view(), name='order-detail'),
    path('update/<int:pk>', views.OrderUpdateView.as_view(), name='order-update'),
    path('delete/<int:pk>', views.OrderDeleteView.as_view(), name='order-delete'),
    path('measurement_report_new/<int:order_id>', views.measurement_report_new, name='measurement_report_new'),
    path('measurement_report_detail/<int:order_id>', views.measurement_report_detail, name='measurement_report_detail'),
    path('measurement_report_update/<int:order_id>', views.measurement_report_update, name='measurement_report_update'),
    path('measurement_report_close/<int:order_id>', views.measurement_report_close, name='measurement_report_close'),
]
