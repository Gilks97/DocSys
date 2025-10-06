from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .decorators import hod_required, staff_required, member_required
from .permission_manager import PermissionManager 

@login_required   
def redirect_dashboard(request):
    user = request.user
    
    if user.is_superuser or user.user_type == 1:   # Admin/HOD
        return redirect("admin_home")
    elif user.user_type == 2:   # Staff
        return redirect("staff_home")  
    elif user.user_type == 3:   # Member
        # Check if member has staff privileges
        if hasattr(user, 'members') and user.members.has_staff_privileges:
            return redirect("staff_home")  
        else:
            return redirect("member_home")  # Regular members
    else:
        return redirect("login")


@login_required
@hod_required
def index(request):
    return render(request, "hod_template/home_content.html")

@login_required
@staff_required
def staff_dashboard(request):
    return render(request, "staff_template/staff_home_template.html") 

@login_required
@member_required
def member_dashboard(request):
    return render(request, "member_template/member_home_template.html")