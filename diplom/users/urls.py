from django.contrib.auth.views import LoginView
from django.urls import path
from allauth.account.views import SignupView, LoginView, LogoutView

from users import views

app_name = "users"


urlpatterns = [
    path("complete-profile/", views.complete_profile, name="complete_profile"),
    path("register/", SignupView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
