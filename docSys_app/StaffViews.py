from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from docSys_app.decorators import staff_required
from docSys_app.forms import DocumentForm
from docSys_app.models import Document
from docSys_app.models import Voices, Members, Attendance, AttendanceReport, Staffs, FeedBackStaffs, CustomUser, Houses, NotificationStaffs


def get_staff_context(request, extra_context=None):
    """Common context for all staff views"""
    context = {
        'is_staff_member': (request.user.user_type == 3 and 
                           hasattr(request.user, 'members') and 
                           request.user.members.has_staff_privileges),
        'is_regular_staff': request.user.user_type == 2,
    }
    if extra_context:
        context.update(extra_context)
    return context


@login_required
@staff_required
def staff_home(request):
    """Staff dashboard - dynamic based on user type"""
    
    # Determine user type
    is_staff_member = (request.user.user_type == 3 and 
                      hasattr(request.user, 'members') and 
                      request.user.members.has_staff_privileges)
    
    context = get_staff_context(request, {
        'is_staff_member': is_staff_member,
    })
    
    if is_staff_member:
        return render(request, "staff_template/staff_member_dashboard.html", context)
    else:
        return render(request, "staff_template/staff_home_template.html", context)


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
    
    context = get_staff_context(request, {
        "form": form,
    })
    return render(request, "staff_template/upload_document_staff.html", context)


@login_required
@staff_required
def staff_view_documents(request):
    documents = Document.objects.all().order_by("-uploaded_at")
    context = get_staff_context(request, {
        "documents": documents,
    })
    return render(request, "staff_template/staff_view_documents.html", context)


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

    context = get_staff_context(request, {
        "form": form,
    })
    return render(request, "staff_template/staff_edit_document.html", context)


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
    user = CustomUser.objects.get(id=request.user.id)
    staff = Staffs.objects.get(admin=user)
    context = get_staff_context(request, {
        "user": user,
        "staff": staff,
    })
    return render(request, "staff_template/staff_profile.html", context)


@login_required
@staff_required
def staff_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("staff_profile"))
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address = request.POST.get("address")
        password = request.POST.get("password")
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            staff = Staffs.objects.get(admin=customuser.id)
            staff.address = address
            staff.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("staff_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("staff_profile"))


# VIEWS FOR STAFF MEMBERS TO ACCESS MEMBER FEATURES
@login_required
@staff_required
def staff_member_view_documents(request):
    """Staff members view documents with staff navigation"""
    documents = Document.objects.all().order_by("-uploaded_at")
    context = get_staff_context(request, {
        "documents": documents,
    })
    
    # Use staff member template instead of regular member template
    return render(request, "staff_template/staff_member_view_documents.html", context)


@login_required
@staff_required  
def staff_member_dashboard(request):
    """Allow staff members to access member dashboard"""
    context = get_staff_context(request)
    return render(request, "member_template/member_home_template.html", context)

