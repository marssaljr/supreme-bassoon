from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.
def register(request):
		if request.method=="GET":
				if request.user.is_authenticated:
						return redirect('/')
				return render(request, 'register.html')
		elif request.method=='POST':
				username=request.POST.get('username')
				email=request.POST.get('email')
				password=request.POST.get('password')
				if len(username.strip())==0 or len(email.strip())==0 or len(password.strip())==0:
						return redirect('/user/register')
				user=User.objects.filter(username=username)
				if user.exists():
						return redirect('/user/register')
				try:
						user=User.objects.create_user(username=username, email=email, password=password)
						user.save()
						return redirect('/user/login')
				except:
						return redirect('/user/register')

def login(request):
		if request.method=='GET':
				if request.user.is_authenticated:
						return redirect('/')
				return render(request,'login.html')
		elif request.method=='POST':
				username=request.POST.get('username')
				password=request.POST.get('password')
				user=auth.authenticate(username=username, password=password)
				if not user:
						return redirect('/user/login')
				else:
						auth.login(request, user)
						return redirect('/')

def logout(request):
		auth.logout(request)
		return redirect('/user/login')
