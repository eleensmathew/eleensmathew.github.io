from django.contrib import admin
from django.urls import path
from . import views
app_name = "webadmin"

#from .views import
urlpatterns = [
    path('stream_video/', views.stream_video, name='stream_video'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]