from django.contrib.auth import get_user_model
from django.db.models import Exists, OuterRef, Q
from django.shortcuts import redirect, render

from allauth.account.forms import ResetPasswordForm
from allauth.account.models import EmailAddress

from users.forms import AdminUserCreationForm, ProfileUpdateForm
from users.models import CustomUser

User = get_user_model()


def complete_profile(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("orders:index")
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, "account/complete_profile.html", {"form": form})


def admin_create_user(request):
    if not request.user.is_authenticated or request.user.role != "admin":
        return redirect("users:login")

    query = request.GET.get("q", "")

    # Подзапрос: ищем подтверждённый email для каждого пользователя
    email_verified_subquery = EmailAddress.objects.filter(
        user=OuterRef('pk'),
        email=OuterRef('email'),
        verified=True
    )

    # Берём пользователей сразу с аннотацией
    users = (
        CustomUser.objects
        .all()
        .annotate(is_email_verified=Exists(email_verified_subquery))
        .prefetch_related('emailaddress_set')  # на случай, если захочется детали почт
    )
    if query:
        users = users.filter(
            Q(email__icontains=query) |
            Q(full_name__icontains=query)
        )

    # Обработка формы создания (без изменений)
    if request.method == "POST":
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            temp_password = CustomUser.objects.make_random_password()
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

    return render(request, "account/admin_create_user.html", {
        "form": form,
        "users": users,
        "query": query,
    })

def send_password_set_email(request, user):
    """Корректно отправляем письмо для установки пароля"""
    form = ResetPasswordForm({"email": user.email})
    if form.is_valid():
        form.save(request=request, use_https=request.is_secure())
