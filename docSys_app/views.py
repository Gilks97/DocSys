from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def redirect_dashboard(request):
    user = request.user
    if user.is_superuser or str(user.user_type) == "1":   # Admin/HOD
        return redirect("index")   # URL name
    elif str(user.user_type) == "2":   # Staff
        return redirect("staff_dashboard")   # redirect by URL name
    elif str(user.user_type) == "3":   # Member
        return redirect("member_dashboard")  # redirect by URL name
    else:
        return redirect("login")   # fallback


@login_required
def index(request):
    return render(request, "hod_template/home_content.html")


@login_required
def staff_dashboard(request):
    return render(request, "staff_template/staff_home_template.html") 


@login_required
def member_dashboard(request):
    return render(request, "member_template/member_home_template.html")
