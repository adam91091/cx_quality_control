from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    path('', views.OrderListView.as_view(), name='orders-list'),
    path('new/', views.OrderCreateView.as_view(), name='order-new'),
    path('detail/<int:pk>', views.OrderDetailView.as_view(), name='order-detail'),
    path('update/<int:pk>', views.OrderUpdateView.as_view(), name='order-update'),
    path('delete/<int:pk>', views.OrderDeleteView.as_view(), name='order-delete'),
    path('measurement-report-new/<int:pk>', views.MeasurementReportCreateView.as_view(), name='measurement-report-new'),
    path('measurement-report-detail/<int:pk>', views.MeasurementReportDetailView.as_view(),
         name='measurement-report-detail'),
    path('measurement-report-update/<int:pk>', views.MeasurementReportUpdateView.as_view(),
         name='measurement-report-update'),
    path('measurement-report-close/<int:pk>', views.MeasurementReportCloseView.as_view(),
         name='measurement-report-close'),
]
