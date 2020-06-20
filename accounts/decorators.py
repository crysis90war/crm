from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts-dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper_func


def allowed_user(allowed_roles=[]):
    def decorators(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)

            else:
                messages.success(request, f'You are not authorized to view this page !')
        return wrapper_func
    return decorators


def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'customer':
            messages.warning(request, f'You are not authorized to view this page !')
            return redirect('accounts-user-pages')

        if group == 'admin':
            return view_func(request, *args, **kwargs)

    return wrapper_function