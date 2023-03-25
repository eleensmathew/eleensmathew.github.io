from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
app_name = "webadmin"

#from .views import
urlpatterns = [
    path('', views.stream_video, name='stream_video'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]
# if settings.DEBUG:
#     urlpatterns += static("", document_root=settings.BASE_DIR / "webadmin/vids")