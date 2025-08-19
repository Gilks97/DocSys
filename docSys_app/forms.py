from django import forms
from django.contrib.auth.models import User
from .models import Profile, Document

class UserEditForm(forms.ModelForm):
    # Users can see (read-only) username & email, but not change them
    username = forms.CharField(disabled=True, required=False)
    email = forms.EmailField(disabled=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']  # only names editable

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'department']

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'description', 'file', 'is_public', 'allowed_users']
        widgets = {
            'allowed_users': forms.CheckboxSelectMultiple
        }
