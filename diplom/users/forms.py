from django import forms
from django.contrib.auth import get_user_model
from allauth.account.forms import SignupForm


User = get_user_model()


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("full_name", "group", "birth_date")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.instance

        placeholders = {
            "full_name": "Введите ФИО",
            "group": "Введите группу",
            "birth_date": "Введите дату рождения (ДД.ММ.ГГ)",
        }
        for field_name, placeholder in placeholders.items():
            if field_name in self.fields:
                self.fields[field_name].widget.attrs["placeholder"] = placeholder

        fields_to_hide_by_role = {
            "admin": ["group", "birth_date"],
            "secretary": ["group", "birth_date"],
        }

        role = getattr(user, "role", None)
        fields_to_hide = fields_to_hide_by_role.get(role, [])

        for field_name in fields_to_hide:
            self.fields.pop(field_name, None)


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

        self.fields["email"].widget.attrs["placeholder"] = "Введите email"

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
