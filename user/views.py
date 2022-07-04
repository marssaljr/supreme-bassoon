from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from user.models import Profile
from django.contrib import auth

# Create your views here.
def register(request):
    request.session["error"] = ""
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("/")
        return render(request, "register.html")
    elif request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        if (
            len(username.strip()) == 0
            or len(email.strip()) == 0
            or len(password.strip()) == 0
        ):
            request.session["error"] = "Email, Senha ou Usuario nao foi digitado!"
            return redirect("/user/register")
        user = User.objects.filter(username=username)
        if user.exists():
            request.session["error"] = "Usuario ja existe!"
            return redirect("/user/register")
        try:
            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            user.save()
            user = auth.authenticate(username=username, password=password)
            if not user:
                return redirect("/user/login")
            else:
                auth.login(request, user)
                profile = Profile.objects.create(user=user)
                profile.save()
                request.session["error"] = "Usuario registrado!"
                return redirect("/")
        except:
            return redirect("/user/register")


def login(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("/")
        return render(request, "login.html")
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(username=username, password=password)
        if not user:
            return redirect("/user/login")
        else:
            auth.login(request, user)
            return redirect("/")


def logout(request):
    auth.logout(request)
    return redirect("/user/login")


@login_required(login_url="/user/login")
def profile(request):
    user = Profile.objects.get(user=request.user)
    return render(request, "profile.html", {"user": user})
