from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total 

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class Supplier(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="nombre", max_length=50)
    last_name = models.CharField(verbose_name="apellido", max_length=50)
    tel = models.CharField(verbose_name="telefono", max_length=50)
    address = models.CharField(verbose_name="direccion", max_length=100)
    email = models.EmailField(verbose_name="correo", max_length=100)
    documentation = models.CharField(verbose_name="documento", max_length=100)
    description = models.TextField(verbose_name="Descripcion", null=True)

    def __str__(self):
        return self.name 

class CategoryProduct(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="nombre")
    description = models.TextField(
        max_length=200, verbose_name="descripcion", null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="nombre")
    image = models.ImageField(
        upload_to='image/', verbose_name="imagen", null=True)
    description = models.TextField(verbose_name="Descripcion", null=True)
    price = models.FloatField(max_length=100, null=True, verbose_name="precio")
    date_end = models.DateField(null=True, verbose_name="fecha de vencimiento")
    category = models.ForeignKey(CategoryProduct, on_delete=models.CASCADE, default=True, null=False, verbose_name="categoria")
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, default=True, null=False, verbose_name="proveedor")
    amount = models.IntegerField(null=True, verbose_name="cantidad")
    digital = models.BooleanField(default=False,null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    lote = models.IntegerField(null=True, verbose_name="lote")

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        self.image.storage.delete(self.image.name)
        super().delete()
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    department = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address