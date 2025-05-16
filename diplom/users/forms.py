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

        self.fields["group"].required = False
        self.fields["group"].widget.attrs[
            "placeholder"
        ] = "Группа (только для студентов)"


    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get("role")
        group = cleaned_data.get("group")

        if role != "student" and group:
            cleaned_data["group"] = "" 

        if role == "student" and not group:
            self.add_error("group", "Группа обязательна для студентов")

        return cleaned_data
    