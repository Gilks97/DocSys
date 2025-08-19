from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserEditForm, ProfileForm, DocumentUploadForm
from .models import Document

#def index(request):
    #return HttpResponse("Hello World")

def showIndexPage(request):
    return render (request, "index.html")

@login_required
def documents_list(request):
    qs = Document.objects.filter(
        Q(is_public=True) | Q(allowed_users=request.user)
    ).distinct()
    return render(request, 'documents_list.html', {'documents': qs})

@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        uform = UserEditForm(request.POST, instance=user)
        pform = ProfileForm(request.POST, instance=user.profile)
        if uform.is_valid() and pform.is_valid():
            # username/email are disabled, so only names + profile fields save
            uform.save()
            pform.save()
            messages.success(request, 'Profile updated.')
            return redirect('profile')
    else:
        uform = UserEditForm(instance=user)
        pform = ProfileForm(instance=user.profile)
    return render(request, 'profile.html', {'uform': uform, 'pform': pform})

def is_admin(user):
    return user.is_staff  # mark your admins with is_staff in Django admin

@user_passes_test(is_admin)
@login_required
def document_upload(request):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.uploaded_by = request.user
            doc.save()
            form.save_m2m()
            messages.success(request, 'Document uploaded.')
            return redirect('documents')
    else:
        form = DocumentUploadForm()
    return render(request, 'document_upload.html', {'form': form})