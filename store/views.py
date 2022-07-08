from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from .models import Product


def home(request):
    medicine = request.GET.get("q")
    if medicine:
        medicine = medicine.capitalize()
        medicines = Product.objects.filter(name__icontains=medicine)
    else:
        medicines = Product.objects.all()
    return render(request, "home.html", {"medicines": medicines})


@login_required(login_url="/user/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("home")


@login_required(login_url="/user/login")
def item_inc(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/user/login")
def item_dec(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/user/login")
def item_rem(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/user/login")
def cart_detail(request):
    cart = Cart(request)
    total = cart.get_total_price()
    print(cart)
    for items in cart:
        print(items)
    return render(request, "cart_detail.html", {'cart': cart, 'total':total})


@login_required(login_url="/user/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")
