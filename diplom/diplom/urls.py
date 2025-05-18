from django.contrib import admin
from django.urls import path, include

from users.views import redirect_by_role

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("accounts/", include("users.urls", namespace="users")),
    path("orders/", include("orders.urls", namespace="orders")),
    path("", redirect_by_role, name="redirect_by_role"),
]
