from importlib.metadata import requires
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django. contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.http import JsonResponse
import json
import datetime

# Create your views here.
from .models import *
from .forms import *
from .decorators import unauthenticated_user, allowed_user, admin_only
from .utils import cookieCart, cartData, guestOrder

""" Mostrando archivo html de la barra de navegacion """

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
@admin_only
def home(request):
    return render(request, 'pages/home.html')


def category(request):
    return render(request, 'pages/category.html')


def list_products(request):
    showProducts = Product.objects.all()
    categories = CategoryProduct.objects.all()

    data = cartData(request)
    order = data['order']

    context = {'showProducts': showProducts, 'categories': categories, 'order':order}
    return render(request, 'pages/list_products.html', context)


def about_us(request):
    return render(request, 'pages/about_us.html')


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    context = {'products': products, }
    return render(request, 'products/index.html', context)


""" Mostrando CRUD Productos """


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def create(request):
    # request.FILES or None || resepciona archivos o imagenes en el CRUD
    formulario = productForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('products')
    return render(request, 'products/create.html', {'formulario': formulario})


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def edit(request, id):
    product = Product.objects.get(id=id)
    formulario = productForm(request.POST or None, request.FILES or None, instance=product)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('products')
    return render(request, 'products/edit.html', {'formulario': formulario})


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def eliminar(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect('products')


""" Mostrando login,register y logout """


@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('list_products')
        else:
            messages.info(request, 'nombre de usuario o contraseña incorrecto')

    context = {}
    return render(request, 'users/login.html', context)


def logoutPage(request):
    logout(request)
    return redirect('list_products')


@unauthenticated_user
def registerPage(request):
    form = UserRegisterForm()

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']

            group = Group.objects.get(name='customer')
            user.groups.add(group)

            messages.success(request, f'Usuario {username} creado')

            return redirect('login')
    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request, 'users/register.html', context)


""" Mostrando E-commerce """


def CategoryView(request, cats):
    category_product = Product.objects.filter(category__name=cats)
    data = cartData(request)
    order = data['order']
    context = {'cats':cats, 'category_product':category_product, 'order':order,}

    return render(request, 'pages/category.html', context)


def details_product(request, pk_test):
    selectProduct = Product.objects.get(id=pk_test)
    showProducts = Product.objects.all()
    showProduct = productDetails(request.POST or None, request.FILES or None, instance=selectProduct)
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'selectProduct': selectProduct,'items':items, 'order':order, 'cartItems':cartItems, 'showProduct':showProduct, 'showProducts': showProducts}
    return render(request, 'ecommerce/details_product.html', context)


@login_required(login_url='login')
def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'ecommerce/cart.html', context)


@login_required(login_url='login')
def checkout(request):
    data = cartData(request)
    
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
    context = {'items':items, 'order':order, 'cartItems':cartItems,}
    return render (request, 'ecommerce/checkout.html', context)


@login_required(login_url='login')
def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)


@login_required(login_url='login')
def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		department=data['shipping']['department'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)


@login_required(login_url='login')
def invoice(request):
    data = cartData(request)
    
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']


    context = {'items':items, 'order':order, 'cartItems':cartItems,}
    return render(request, 'ecommerce/invoice.html', context)

""" Mostrando Categorias """


@login_required(login_url='login')
def categories(request):
    categories = CategoryProduct.objects.all()
    context = {'categories': categories, }

    return render(request, 'categories/index.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def createCategory(request):
    categories = CategoryProductFrom(
        request.POST or None, request.FILES or None)
    if categories.is_valid():
        categories.save()
        return redirect('categories')
    context = {'categories': categories}
    return render(request, 'categories/createCategory.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def editCategory(request, id):
    categories = CategoryProduct.objects.get(id=id)
    categories = CategoryProductFrom(
        request.POST or None, request.FILES or None, instance=categories)
    if categories.is_valid() and request.POST:
        categories.save()
        return redirect('categories')
    return render(request, 'categories/editCategory.html', {'categories': categories})


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def eliminarCategory(request, id):
    categories = CategoryProduct.objects.get(id=id)
    categories.delete()
    return redirect('categories')


""" Mostrando Proveedeores """

@login_required(login_url='login')
def suppliers(request):
    suppliers = Supplier.objects.all()
    context = {'suppliers': suppliers, }

    return render (request, 'suppliers/index.html', context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def createSupplier(request):
    suppliers = supplierForm(request.POST or None, request.FILES or None)
    if suppliers.is_valid():
        suppliers.save()
        return redirect('suppliers')
    context = {'suppliers': suppliers}
    return render(request, 'suppliers/createSupplier.html', context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def editSupplier(request, id):
    suppliers = Supplier.objects.get(id=id)
    suppliers = supplierForm(request.POST or None, request.FILES or None, instance=suppliers)
    if suppliers.is_valid() and request.POST:
        suppliers.save()
        return redirect('suppliers')
    return render(request, 'suppliers/editSupplier.html', {'suppliers': suppliers})

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def deleteSupplier(request, id):
    suppliers = Supplier.objects.get(id=id)
    suppliers.delete()
    return redirect('suppliers')
