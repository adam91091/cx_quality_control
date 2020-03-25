from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.products_list, name='products_list'),
    path('new/', views.product_new, name='product_new'),
    path('detail/<int:product_id>', views.product_detail, name='product_detail'),
    path('update/<int:product_id>', views.product_update, name='product_update'),
    path('delete/<int:product_id>', views.product_delete, name='product_delete'),
]
