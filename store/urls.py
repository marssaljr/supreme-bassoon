from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
		re_path(r'cart/add/(?P<id>[0-9]+)', views.cart_add, name='cart_add'),
		path('cart/cart-detail/',views.cart_detail,name='cart_detail'),
		path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
		re_path(r'cart/dec/(?P<id>[0-9]+)', views.item_dec, name='cart_dec'),
		re_path(r'cart/inc/(?P<id>[0-9]+)', views.item_inc, name='cart_inc'),
		re_path(r'cart/rem/(?P<id>[0-9]+)', views.item_rem, name='cart_rem'),
]
