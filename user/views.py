from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from user.forms import ProfileForm
from .models import Profile
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

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

@login_required(login_url="/users/login")
def profile(request):
		if request.method=='GET':
			userId=request.user.id
			user=Profile.objects.get(id=userId)
			return render(request,'profile.html')
		elif request.method=='POST':
			form = ProfileForm(request.POST, request.FILES)
			if form.is_valid():
				print('is valid')
				form.save()
				#upload=Profile(photo=request.FILES['photo'])
				#upload.save()
			else:
				print('isn\'t valid')
				form = ProfileForm()
			return redirect('/user/profile',{'form': form})
