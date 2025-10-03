from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from docSys_app.decorators import staff_required
from docSys_app.forms import DocumentForm
from docSys_app.models import Document
from docSys_app.models import Voices, Members, Attendance, AttendanceReport, Staffs, FeedBackStaffs, CustomUser, Houses, NotificationStaffs


@login_required
@staff_required
def staff_home(request):
    return render(request,"staff_template/staff_home_template.html")

@login_required
@staff_required
def upload_document_staff(request):
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.uploaded_by = request.user
            doc.save()
            messages.success(request, "Document uploaded successfully.")
            return redirect("staff_view_documents")
    else:
        form = DocumentForm()
    return render(request, "staff_template/upload_document_staff.html", {"form": form})

@login_required
@staff_required
def staff_view_documents(request):
    documents = Document.objects.all().order_by("-uploaded_at")
    return render(request, "staff_template/staff_view_documents.html", {"documents": documents})
# Edit document (Staff)

@login_required
@staff_required
def staff_edit_document(request, doc_id):
    doc = get_object_or_404(Document, id=doc_id)

    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES, instance=doc)
        if form.is_valid():
            form.save()
            messages.success(request, "Document updated successfully.")
            return redirect("staff_view_documents")
    else:
        form = DocumentForm(instance=doc)

    return render(request, "staff_template/staff_edit_document.html", {"form": form})


# Delete document (Staff)
@login_required
@staff_required
def staff_delete_document(request, doc_id):
    doc = get_object_or_404(Document, id=doc_id)
    doc.delete()
    messages.success(request, "Document deleted successfully.")
    return redirect("staff_view_documents")

@login_required
@staff_required
def staff_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    staff=Staffs.objects.get(admin=user)
    return render(request,"staff_template/staff_profile.html",{"user":user,"staff":staff})


@login_required
@staff_required
def staff_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("staff_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        address=request.POST.get("address")
        password=request.POST.get("password")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password!=None and password!="":
                customuser.set_password(password)
            customuser.save()

            staff=Staffs.objects.get(admin=customuser.id)
            staff.address=address
            staff.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("staff_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("staff_profile"))
        

