from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from docSys_app import views, HodViews, StaffViews, MemberViews
from docSys import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    # Root URL goes to login page
    path('', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),

    # Authentication URLs (login, logout, password reset, etc.)
    path('accounts/', include('django.contrib.auth.urls')),

    # Include your app URLs (make sure app name is correct)
    path('', include('docSys_app.urls')),

    path('admin_home',HodViews.admin_home,name="admin_home"),
    path('add_staff',HodViews.add_staff,name="add_staff"),
    path('add_staff_save',HodViews.add_staff_save,name="add_staff_save"),
    path('add_house', HodViews.add_house,name="add_house"),
    path('add_house_save', HodViews.add_house_save,name="add_house_save"),
    path('add_member', HodViews.add_member,name="add_member"),
    path('add_member_save', HodViews.add_member_save,name="add_member_save"),
    path('add_voice', HodViews.add_voice,name="add_voice"),
    path('add_voice_save', HodViews.add_voice_save,name="add_voice_save"),
    path('manage_staff', HodViews.manage_staff,name="manage_staff"),
    path('manage_member', HodViews.manage_member,name="manage_member"),
    path('manage_house', HodViews.manage_house,name="manage_house"),
    path('manage_voice', HodViews.manage_voice,name="manage_voice"),
    path('edit_staff/<str:staff_id>', HodViews.edit_staff,name="edit_staff"),
    path('edit_staff_save', HodViews.edit_staff_save,name="edit_staff_save"),
    path("delete_staff/<int:staff_id>/", HodViews.delete_staff, name="delete_staff"),
    path('edit_member/<str:member_id>', HodViews.edit_member,name="edit_member"),
    path('edit_member_save', HodViews.edit_member_save,name="edit_member_save"),
    path("delete_member/<int:member_id>/", HodViews.delete_member, name="delete_member"),
    path('edit_voice/<str:voice_id>', HodViews.edit_voice,name="edit_voice"),
    path('edit_voice_save', HodViews.edit_voice_save,name="edit_voice_save"),
    path('delete_voice/<int:voice_id>/', HodViews.delete_voice, name='delete_voice'),
    path('edit_house/<str:house_id>', HodViews.edit_house,name="edit_house"),
    path('edit_house_save', HodViews.edit_house_save,name="edit_house_save"),
    path('delete_house/<int:house_id>/', HodViews.delete_house, name='delete_house'),

    path('staff_home', StaffViews.staff_home, name="staff_home"),
    path('member_home', MemberViews.member_home, name="member_home"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
