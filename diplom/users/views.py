from django.shortcuts import render, redirect

from users.forms import ProfileUpdateForm


def complete_profile(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("orders:create_order")
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, "users/complete_profile.html", {"form": form})
