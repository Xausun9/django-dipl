from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # username мы используем как email
        email = username or kwargs.get('email')
        if email is None or password is None:
            return None

        # вместо .objects.get() используем ._default_manager.filter().first()
        user = UserModel._default_manager.filter(email=email).first()
        if user is None:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
