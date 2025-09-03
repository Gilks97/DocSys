from django.contrib import admin
from .models import Document

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from docSys_app.models import CustomUser


class UserModel(UserAdmin):
    pass

admin.site.register(CustomUser,UserModel)

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "uploaded_by", "uploaded_at")
    search_fields = ("title", "uploaded_by__username")