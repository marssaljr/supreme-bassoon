from django.shortcuts import render
from .models import Product

# Create your views here.
def home(request):
	medicines = Product.objects.all()
	return render(request, 'home.html', {'medicines': medicines})
