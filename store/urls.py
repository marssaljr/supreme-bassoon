from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
		path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
]
