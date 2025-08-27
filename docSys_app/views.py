from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def redirect_dashboard(request):
    user = request.user
    if user.is_superuser or user.user_type == "1":   # HOD/Admin
        return redirect("index")   # your index view name/url
    elif user.user_type == "2":   # Staff
        return redirect("staff_dashboard")  # define later
    elif user.user_type == "3":   # Member
        return redirect("member_dashboard")  # define later
    else:
        return redirect("login")


@login_required
def index(request):
    return render(request, "hod_template/home_content.html")   # make sure you create templates/index.html


@login_required
def staff_dashboard(request):
    return render(request, "staff_dashboard.html")  # create this template too


@login_required
def member_dashboard(request):
    return render(request, "member_dashboard.html")  # create this template too