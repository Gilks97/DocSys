from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from .permission_manager import PermissionManager  # 🆕 ADD THIS IMPORT

class LoginRequiredMiddleware:
    """
    Middleware to ensure all pages require login except whitelisted URLs.
    """
    def __init__(self, get_response):
        self.get_response = get_response
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
            user_type = request.user.user_type
            current_path = request.path
            
            # USE PERMISSION MANAGER FOR ALL CHECKS
            is_hod = PermissionManager.is_hod(request.user)
            has_staff_access = PermissionManager.has_staff_privileges(request.user)
            is_member = PermissionManager.is_member(request.user)

            # Define URL access rules
            access_rules = {
                '/index/': is_hod,
                '/staff/dashboard/': has_staff_access,
                '/member/dashboard/': is_member,
                '/admin_home': is_hod,
                '/staff_home': has_staff_access,
                '/member_home': is_member,
            }

            # Check if current path has access rules
            for path, has_access in access_rules.items():
                if current_path == path and not has_access:
                    return self._redirect_to_proper_dashboard(request.user)

        return self.get_response(request)

    def _redirect_to_proper_dashboard(self, user):
        """Redirect user to their appropriate dashboard"""
        if PermissionManager.is_hod(user):
            return redirect('index')
        elif PermissionManager.has_staff_privileges(user):
            return redirect('staff_home')
        elif PermissionManager.is_member(user):
            return redirect('member_home')
        else:
            return redirect('login')