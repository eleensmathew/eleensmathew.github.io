from django.contrib import admin
from .models import Admin_info, PriorityQueue, CustomUser

admin.site.register(Admin_info)
admin.site.register(PriorityQueue)
admin.site.register(CustomUser)