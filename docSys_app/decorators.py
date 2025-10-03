from django.http import HttpResponseForbidden
from django.shortcuts import redirect

def hod_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == 1:
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("Access denied: HOD privileges required")
    return wrapper

def staff_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == 2:
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("Access denied: Staff privileges required")
    return wrapper

def member_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == 3:
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("Access denied: Member privileges required")
    return wrapper