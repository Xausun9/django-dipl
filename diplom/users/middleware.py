from django.shortcuts import redirect
from django.urls import reverse

class CompleteProfileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated:
            needs_full_name = not user.full_name
            needs_group = user.role == 'student' and not user.group

            if needs_full_name or needs_group:
                complete_profile_url = reverse('users:complete_profile')
                if request.path != complete_profile_url:
                    return redirect(complete_profile_url)

        response = self.get_response(request)
        return response
