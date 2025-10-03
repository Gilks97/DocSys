from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

class LoginRequiredMiddleware:
    """
    Middleware to ensure all pages require login except whitelisted URLs.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # Using settings.LOGIN_URL & LOGOUT_REDIRECT_URL for consistency
        self.public_paths = [
            settings.LOGIN_URL,
            settings.LOGOUT_REDIRECT_URL,
        ]

    def __call__(self, request):
        if not request.user.is_authenticated and request.path not in self.public_paths:
            return redirect(settings.LOGIN_URL.lstrip('/'))
        return self.get_response(request)


class RoleRequiredMiddleware:
    """
    Redirect users trying to access another role's dashboard.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            user_type = str(request.user.user_type)

            # HOD/Admin
            if request.path.startswith("/admin/") and user_type != "1":
                return redirect('staff_dashboard' if user_type == "2" else 'member_dashboard')

            # Staff
            if request.path.startswith("/staff/") and user_type != "2":
                return redirect('index' if user_type == "1" else 'member_dashboard')

            # Member
            if request.path.startswith("/member/") and user_type != "3":
                return redirect('index' if user_type == "1" else 'staff_dashboard')

        return self.get_response(request)
