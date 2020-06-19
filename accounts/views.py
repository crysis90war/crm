from django.shortcuts import render, redirect
from accounts.models import *
from accounts.forms import *
# Create your views here.


def home(request):
    context = {
        'title': 'Dashboard',
        'orders': Order.objects.all().order_by('-created_at'),
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


def createOrder(request):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts-dashboard')

    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('accounts-dashboard')

    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('accounts-dashboard')
    context = {'item': order}
    return render(request, 'accounts/delete.html', context)