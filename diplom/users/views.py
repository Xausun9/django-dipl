from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from users.forms import LoginForm, RegistrationForm
from django.contrib.auth.models import User


def login_view(request):
    if request.user.is_authenticated:
        return redirect("orders:index")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_page = request.GET.get("next", reverse("orders:index"))
                return redirect(next_page)
            else:
                messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()

    return render(request, "users/login.html", {"form": form, "title": "Sign In"})


def register_view(request):
    if request.user.is_authenticated:
        return redirect("orders:index")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            user.save()
            messages.success(request, "Congratulations, you are now a registered user!")
            return redirect("users:login")
    else:
        form = RegistrationForm()

    return render(request, "users/register.html", {"form": form, "title": "Register"})


@login_required
def logout_view(request):
    logout(request)
    return redirect("orders:index")
