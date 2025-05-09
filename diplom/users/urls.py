from django.contrib.auth.views import LoginView
from django.urls import path
from users import views
from users.forms import EmailAuthenticationForm

app_name = 'users'


urlpatterns = [
    path('register/', views.register, name='register'),
    path('complete-profile/', views.complete_profile, name='complete_profile'),
    path('login/', LoginView.as_view(
        template_name='users/login.html',
        authentication_form=EmailAuthenticationForm
    ), name='login'),
    path('logout/', views.logout_view, name='logout'),
]