from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    # path('', views.clients_list, name='clients-list'),
    path('', views.ClientListView.as_view(), name='clients-list'),
    path('new/', views.ClientCreateView.as_view(), name='client-new'),
    path('detail/<int:pk>', views.ClientDetailView.as_view(), name='client-detail'),
    path('update/<int:pk>', views.ClientUpdateView.as_view(), name='client-update'),
    path('delete/<int:pk>', views.ClientDeleteView.as_view(), name='client-delete'),
]
