from django import forms
from django.contrib.auth import get_user_model, authenticate


User = get_user_model()


# class UserRegistrationForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
#     password2 = forms.CharField(
#         widget=forms.PasswordInput, label="Подтверждение пароль"
#     )

#     class Meta:
#         model = User
#         fields = ("email",)

#     def clean_password2(self):
#         password = self.cleaned_data.get("password")
#         password2 = self.cleaned_data.get("password2")
#         if password and password2 and password != password2:
#             raise forms.ValidationError("Пароли не совпадают")
#         return password2


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("full_name", "group")


# class EmailAuthenticationForm(forms.Form):
#     email = forms.EmailField(label="Email")
#     password = forms.CharField(label="Пароль", strip=False, widget=forms.PasswordInput)

#     error_messages = {
#         "invalid_login": "Пожалуйста, введите правильный email и пароль.",
#         "inactive": "Этот аккаунт неактивен.",
#     }

#     def __init__(self, request=None, *args, **kwargs):
#         self.request = request
#         self.user_cache = None
#         super().__init__(*args, **kwargs)

#     def clean(self):
#         email = self.cleaned_data.get("email")
#         password = self.cleaned_data.get("password")

#         if email and password:
#             self.user_cache = authenticate(self.request, username=email, password=password)
#             if self.user_cache is None:
#                 raise forms.ValidationError(
#                     self.error_messages["invalid_login"],
#                     code="invalid_login",
#                 )
#             else:
#                 self.confirm_login_allowed(self.user_cache)

#         return self.cleaned_data

#     def confirm_login_allowed(self, user):
#         if not user.is_active:
#             raise forms.ValidationError(
#                 self.error_messages["inactive"],
#                 code="inactive",
#             )

#     def get_user(self):
#         return self.user_cache
