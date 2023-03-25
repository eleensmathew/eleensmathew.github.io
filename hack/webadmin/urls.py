from django.contrib import admin
from django.urls import path
from . import views
app_name = "webadmin"

#from .views import
urlpatterns = [
    path('get_video/', views.get_video, name='get_video'),
]