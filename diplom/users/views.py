from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Exists, OuterRef, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from allauth.account.forms import ResetPasswordForm
from allauth.account.models import EmailAddress

from users.forms import AdminUserCreationForm, ProfileUpdateForm


User = get_user_model()


@login_required
def redirect_by_role(request):
    user = request.user

    if user.role == "student":
        return redirect("orders:create_order")
    elif user.role == "secretary":
        return redirect("orders:secretary")
    elif user.role == "admin":
        return redirect("users:admin_create_user")


@login_required
def complete_profile(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("redirect_by_role")
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, "account/complete_profile.html", {"form": form})


@login_required
def admin_create_user(request):
    if not request.user.is_authenticated or request.user.role != "admin":
        return redirect("users:login")

    query = request.GET.get("q", "")

    if request.method == "POST" and "delete_user_id" in request.POST:
        user_id = request.POST.get("delete_user_id")
        user_to_delete = get_object_or_404(User, id=user_id)
        if user_to_delete != request.user:
            user_to_delete.delete()
        return redirect("users:admin_create_user")

    if request.method == "POST" and "create_user" in request.POST:
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            temp_password = User.objects.make_random_password()
            user.set_password(temp_password)
            user.is_active = True
            user.save()

            EmailAddress.objects.create(
                user=user, email=user.email, verified=True, primary=True
            )

            send_password_set_email(request, user)
            return redirect("users:admin_create_user")
    else:
        form = AdminUserCreationForm()

    email_verified_subquery = EmailAddress.objects.filter(
        user=OuterRef("pk"), email=OuterRef("email"), verified=True
    )

    users = (
        User.objects.all().order_by("group")
        .annotate(is_email_verified=Exists(email_verified_subquery))
        .prefetch_related("emailaddress_set")
    )
    if query:
        users = users.filter(Q(email__icontains=query) | Q(full_name__icontains=query))

    return render(
        request,
        "account/admin_create_user.html",
        {
            "form": form,
            "users": users,
            "query": query,
        },
    )


def send_password_set_email(request, user):
    form = ResetPasswordForm({"email": user.email})
    if form.is_valid():
        form.save(request=request, use_https=request.is_secure())


@login_required
@require_POST
def delete_user_ajax(request):
    if request.user.role != "admin":
        return JsonResponse(
            {"success": False, "error": "Недостаточно прав"}, status=403
        )

    user_id = request.POST.get("user_id")
    if not user_id:
        return JsonResponse(
            {"success": False, "error": "Не указан пользователь"}, status=400
        )

    user_to_delete = get_object_or_404(User, id=user_id)

    if user_to_delete == request.user:
        return JsonResponse(
            {"success": False, "error": "Нельзя удалить самого себя"}, status=400
        )

    user_to_delete.delete()
    return JsonResponse({"success": True})
