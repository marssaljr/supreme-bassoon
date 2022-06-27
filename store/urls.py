from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
		path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
		path('cart/cart-detail/',views.cart_detail,name='cart_detail'),
		path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
]
