from django import forms
from django.contrib.auth import get_user_model
from allauth.account.forms import SignupForm


User = get_user_model()


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("full_name", "group")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        user = self.instance
        if user.role in ['secretary', 'admin']:
            self.fields.pop('group')


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        user.role = "student"
        user.save()
        return user


class AdminUserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "role", "group"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Скрываем поле "group", если роль != student
        self.fields["group"].required = False
        self.fields["group"].widget.attrs[
            "placeholder"
        ] = "Группа (только для студентов)"

        # JavaScript на стороне шаблона тоже можно добавить для динамического скрытия — потом покажу

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get("role")
        group = cleaned_data.get("group")

        if role != "student" and group:
            cleaned_data["group"] = ""  # Очистим group, если роль не student

        if role == "student" and not group:
            self.add_error("group", "Группа обязательна для студентов")

        return cleaned_data


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
