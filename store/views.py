from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from .models import Product

# Create your views here.
def home(request):
	medicines = Product.objects.all()
	return render(request, 'home.html', {'medicines': medicines})

@login_required(login_url="/users/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("home")

@login_required(login_url="/users/login")
def cart_detail(request):
    return render(request, 'cart_detail.html')

@login_required(login_url="/users/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")
