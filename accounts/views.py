from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from accounts.forms import *
from .filters import OrderFilter
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

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {
        'title': 'Customer',
        'customer': customer,
        'orders': orders,
        'order_count': order_count,
        'myFilter' : myFilter
    }
    return render(request, 'accounts/customer.html', context)


def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'))
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    #form = OrderForm(initial={'customer': customer})

    if request.method == 'POST':
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('accounts-dashboard')

    context = {'formset': formset}
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