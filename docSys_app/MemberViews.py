from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from docSys_app.decorators import member_required
from docSys_app.models import Document

@login_required
@member_required
def member_home(request):
    return render(request,"member_template/member_home_template.html")


@login_required
@member_required
def member_view_documents(request):
    documents = Document.objects.all().order_by("-uploaded_at")
    return render(request, "member_template/member_view_documents.html", {"documents": documents})
