from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    #address = forms.CharField(label='Direccion')
    #tel_number = forms.IntegerField(label='Telefono')
    class Meta:
        model = User
        fields= ['username', 'email', 'password1', 'password2', "first_name", "last_name"]
        help_texts = {k:"" for k in fields}

class productForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class productDetails(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['image', 'name', 'description', 'price', 'amount', ]

class CategoryProductFrom(forms.ModelForm):
    class Meta:
        model = CategoryProduct
        fields = ['name', 'description', ]

class supplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'

class shippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = '__all__'
