from django.contrib.auth.views import LoginView
from django.urls import path

from allauth.account.views import LoginView, LogoutView, SignupView
from users import views

app_name = "users"


urlpatterns = [
    path("complete-profile/", views.complete_profile, name="complete_profile"),
    path("register/", SignupView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("admin-create-user/", views.admin_create_user, name="admin_create_user"),
    path('delete-user-ajax/', views.delete_user_ajax, name='delete_user_ajax'),

]
