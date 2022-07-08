from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from user.models import Profile
from django.contrib import auth
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return login(request)
        else:
            return redirect("/user/register")
    else:
        form=RegisterForm()
        if request.user.is_authenticated:
            return redirect("home")
    return render(request, 'register.html', {'form':form})

def login(request):
    if request.method == "POST":
        form=LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = auth.authenticate(username=username, password=password)
            if not user:
                return redirect("login")
            else:
                auth.login(request, user)
                Profile.objects.get_or_create(user=user)
                return redirect("home")
    else:
        form=LoginForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    auth.logout(request)
    return redirect("/user/login")

def delete(request):
    if request.method =="GET":
        user=request.user
        if user.is_anonymous:
            return redirect("login")
        return render(request,"delete.html")
    user = request.user
    if user.is_anonymous:
        return redirect("login")
    profile = Profile.objects.filter(user=user)
    user = User.objects.get(pk=user.pk)
    profile.delete()
    user.delete()
    return render(request, "delete.html", {'success':'ok'})

@login_required(login_url="/user/login")
def profile(request):
    if request.method == "POST":
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            request.session["message"] = "Perfil atualizado com sucesso!"
            return redirect(to="profile")
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
        # user = Profile.objects.get(user=request.user)
        # return render(request, "profile.html")
    return render(
        request, "profile.html", {"user_form": user_form, "profile_form": profile_form}
    )
