from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib import auth, messages
from django.shortcuts import render, redirect
from django.views import View

from user.models import Profile
from user.forms import LoginForm, UpdateUserForm, UpdateProfileForm, RegisterForm


class RegisterView(View):
    form_class = RegisterForm
    initial = {"key": "value"}
    template_name = "register.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")

        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}")

            return redirect("/user/login")
        return render(request, self.template_name, {"form": form})


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = "login.html"
    redirect_field_name = "/"
    redirect_authenticated_user = "/"

    def form_valid(self, form):
        return super(CustomLoginView, self).form_valid(form)


def logout(request):
    auth.logout(request)
    return redirect("/user/login")


def delete(request):
    if request.method == "GET":
        user = request.user
        if user.is_anonymous:
            return redirect("login")
        return render(request, "delete.html")
    user = request.user
    if user.is_anonymous:
        return redirect("login")
    profile = Profile.objects.filter(user=user)
    user = User.objects.get(pk=user.pk)
    profile.delete()
    user.delete()
    return render(request, "delete.html", {"success": "ok"})


@login_required(login_url="/user/login")
def profile(request):
    if request.method == "POST":
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f"Perfil atualizado com sucesso!")
            return redirect(to="profile")
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
    return render(
        request, "profile.html", {"user_form": user_form, "profile_form": profile_form}
    )
