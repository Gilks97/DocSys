from django.shortcuts import render


def member_home(request):
    return render(request,"member_template/member_home_template.html")