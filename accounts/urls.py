from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='accounts-dashboard'),
    path('products/', views.products, name='accounts-products'),
    path('customer/', views.customer, name='accounts-customer'),
]