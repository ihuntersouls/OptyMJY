from tokenize import group
from django.http import HttpResponse
from django.shortcuts import redirect

""" No permitir ingresar al login/registro si ya inicio sesion """

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('list_products')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

""" BLoquear acceso a usuarios NoAdmin """

def allowed_user(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('Sesion no autorizada, SALGASEE!')
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'customer':
            return redirect('list_products')

        if group == 'admin':
            return view_func(request, *args, **kwargs)
    return wrapper_function