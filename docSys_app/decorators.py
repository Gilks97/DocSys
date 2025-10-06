from django.http import HttpResponseForbidden
from functools import wraps
from .permission_manager import PermissionManager 


def hod_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if PermissionManager.is_hod(request.user):  # USE PermissionManager
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("Access denied: HOD privileges required")
    return wrapper

def staff_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if PermissionManager.has_staff_privileges(request.user):  # USE PermissionManager
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("Access denied: Staff privileges required")
    return wrapper

def member_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if PermissionManager.is_member(request.user):  # USE PermissionManager
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("Access denied: Member account required")
    return wrapper
