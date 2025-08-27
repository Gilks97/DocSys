from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    #path('', views.showDemoPage, name="demo")
    #path('',views.index, name="index"),
    #path('demo/', views.showDemoPage),
    #path('index/', views.index, name="index"),
    path('redirect_dashboard/', views.redirect_dashboard, name='redirect_dashboard'),
    path('index/', views.index, name='index'),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('member/dashboard/', views.member_dashboard, name='member_dashboard'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])