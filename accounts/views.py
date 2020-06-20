from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Create your views here.
from accounts.forms import *
from .models import *
from .forms import OrderForm, CreateUserForm, ConnectionUserForm
from .filters import OrderFilter


@login_required
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


@login_required
def products(request):
    products = Product.objects.all()

    return render(request, 'accounts/products.html', {'title': 'Products', 'products': products})


@login_required
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


@login_required
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


@login_required
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


@login_required
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('accounts-dashboard')

    context = {'item': order}

    return render(request, 'accounts/delete.html', context)


def registerUser(request):
    if request.user.is_authenticated:
        return redirect('accounts-dashboard')
    else:
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created! You can now able to log in')
            return redirect('login')

        context = {
            'form': form
        }

        return render(request, 'accounts/register.html', context)


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('accounts-dashboard')
    else:
        form = ConnectionUserForm(request.POST)

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('accounts-dashboard')
            else:
                messages.info(request, 'Username or Password Incorrect !')

        context = {'form': form}

        return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')