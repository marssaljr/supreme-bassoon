from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from user.models import Profile
from django.contrib import auth
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm

# Create your views here.
def register(request):
    request.session["error"] = ""
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("/")
        return render(request, "register.html")
    elif request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        if (
            len(username.strip()) == 0
            or len(email.strip()) == 0
            or len(password.strip()) == 0
            or len(first_name.strip()) == 0
            or len(last_name.strip()) == 0
        ):
            request.session["error"] = "Email, Senha ou Usuario nao foi digitado!"
            return redirect("register")
        user = User.objects.filter(username=username)
        if user.exists():
            request.session["error"] = "Usuario ja existe!"
            return redirect("register")
        try:
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password
            )
            user.save()
            request.session["error"]="Usuario criado!"
            #user = auth.authenticate(username=username, password=password)
            if not user:
                return redirect("register")
            else:
                return login(request)
                #auth.login(request, user)
                #profile = Profile.objects.create(user=user)
                #profile.save()
                #return redirect("home")
        except:
            return redirect("/user/register")


def login(request):
    if request.method == "GET":
        #nextRoute=request.GET.get('next')
        if request.user.is_authenticated:
            #return redirect(nextRoute,"home")
            return redirect("home")
        return render(request, "login.html")
    elif request.method == "POST":
        #nextRoute=request.GET.get('next')
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(username=username, password=password)
        if not user:
            return redirect("login")
        else:
            auth.login(request, user)
            profile=Profile.objects.get_or_create(user=user)
            #return redirect(nextRoute, 'home')
            return redirect("home")

def logout(request):
    auth.logout(request)
    return redirect("/user/login")


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
