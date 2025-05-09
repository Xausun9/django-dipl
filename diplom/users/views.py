from django.shortcuts import render, redirect
from django.contrib.auth import login, logout

from users.forms import UserRegistrationForm, ProfileUpdateForm


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)
            return redirect("users:complete_profile")
    else:
        form = UserRegistrationForm()
    return render(request, "users/register.html", {"form": form})


def complete_profile(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("orders:create_order")
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, "users/complete_profile.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("users:login")
