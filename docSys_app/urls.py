from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('', views.showDemoPage, name="demo")
    #path('',views.index, name="index"),
    #path('demo/', views.showDemoPage),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])