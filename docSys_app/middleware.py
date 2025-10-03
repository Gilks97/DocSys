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
    Backup protection for URL manipulation
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            user_type = request.user.user_type  # Use integer directly
            current_path = request.path

            # Quick redirect for obvious URL manipulation
            if current_path == '/index/' and user_type != 1:
                return redirect('staff_dashboard' if user_type == 2 else 'member_dashboard')
            elif current_path == '/staff/dashboard/' and user_type != 2:
                return redirect('index' if user_type == 1 else 'member_dashboard')
            elif current_path == '/member/dashboard/' and user_type != 3:
                return redirect('index' if user_type == 1 else 'staff_dashboard')
            
            # Also protect the "home" URLs from main urls.py
            if current_path == '/admin_home' and user_type != 1:
                return redirect('staff_home' if user_type == 2 else 'member_home')
            elif current_path == '/staff_home' and user_type != 2:
                return redirect('admin_home' if user_type == 1 else 'member_home')
            elif current_path == '/member_home' and user_type != 3:
                return redirect('admin_home' if user_type == 1 else 'staff_home')

        return self.get_response(request)