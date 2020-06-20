from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='accounts-dashboard'),
    path('user/', views.userPage, name='accounts-user-pages'),
    path('products/', views.products, name='accounts-products'),
    path('customer/<str:pk_test>', views.customer, name='accounts-customer'),

    path('create_order/<str:pk>', views.createOrder, name='accounts-create-order'),
    path('update_order/<str:pk>', views.updateOrder, name='accounts-update-order'),
    path('delete_order/<str:pk>', views.deleteOrder, name='accounts-delete-order'),

    path('login/', views.loginUser, name='login'),
    path('register/', views.registerUser, name='register'),
    path('logout/', views.logoutUser, name="logout"),
]