from django.shortcuts import render
from accounts.models import *
# Create your views here.


def home(request):
    context = {
        'title': 'Dashboard',
        'orders': Order.objects.all(),
        'customers': Customer.objects.all(),
        'total_customers': Customer.objects.all().count(),
        'total_orders': Order.objects.all().count(),
        'delivered': Order.objects.filter(status='Delivered').count(),
        'pending': Order.objects.filter(status='Pending').count()
    }

    return render(request, 'accounts/dashboard.html', context)


def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'title': 'Products', 'products': products})


def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    order_count = orders.count()

    context = {
        'title': 'Customer',
        'customer': customer,
        'orders': orders,
        'order_count': order_count
    }
    return render(request, 'accounts/customer.html', context)
