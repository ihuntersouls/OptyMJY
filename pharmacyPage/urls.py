from django.urls import path
from .import views
from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.conf.urls.static import static

urlpatterns=[
    #Redirigiendo las urls del panel de navegacion nav
    path('administer', views.home, name='home'),
    path('category', views.category, name='category'),
    path('', views.list_products, name='list_products'),
    path('about_us', views.about_us, name='about_us'),

    #Rediriengo las ulrs de la seccion del crud de productos
    path('products', views.products, name='products'),
    path('products/create', views.create, name='create'),
    path('products/edit', views.edit, name='edit'),
    path('eliminar/<int:id>', views.eliminar, name='eliminar'),
    path('products/edit/<int:id>', views.edit, name='edit'),

    #Redirigiendo a seccion de loggin y sing up

    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    
    # E-commerce

    path('details_product/<int:pk_test>', views.details_product, name='details_product'),

    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),

    # Categorias
    path('categories', views.categories, name='categories'),
    path('category/<str:cats>/', views.CategoryView, name='category'),

    path('categories/createCategory', views.createCategory, name='createCategory'),
    path('categories/editCategory', views.editCategory, name='editCategory'),
    path('eliminarCategory/<int:id>', views.eliminarCategory, name='eliminarCategory'),
    path('categories/editCategory/<int:id>', views.editCategory, name='editCategory'),

    # Proveedores
    path('suppliers', views.suppliers, name='suppliers'),

    path('suppliers/createSupplier', views.createSupplier, name='createSupplier'),
    path('suppliers/editSupplier', views.editSupplier, name='editSupplier'),
    path('deleteSupplier/<int:id>', views.deleteSupplier, name='deleteSupplier'),
    path('suppliers/editSupplier/<int:id>', views.editSupplier, name='editSupplier'),

    # Factura
    path('invoice', views.invoice, name='invoice'),

    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
