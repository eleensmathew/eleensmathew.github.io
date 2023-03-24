from django.contrib import admin
from django.urls import path
app_name = "user"

from .views import Upload
urlpatterns = [
   
    
    path('upload/', Upload,name="Upload"),

]