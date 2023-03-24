from django.contrib import admin
from django.urls import path
app_name = "user"

from .views import upload_video
urlpatterns = [
   
    
    path('upload/', upload_video,name="upload_video"),

]