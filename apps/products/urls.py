from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.products_list, name='products_list'),
    path('new/', views.ProductCreateView.as_view(), name='product-new'),
    path('detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('update/<int:pk>', views.ProductUpdateView.as_view(), name='product-update'),
    path('delete/<int:pk>', views.ProductDeleteView.as_view(), name='product-delete'),
]
