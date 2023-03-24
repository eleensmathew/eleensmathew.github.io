from django.shortcuts import render
from .models import Priority, Admin_info
import heapq
import copy
from django.db.models import Min
# Create your views here.

def select_admin(): #Selecting which admin should monitor that video recording
    adminsel = Admin_info.objects.all().order_by(-'size').first()
    return adminsel
    
def get_video(request):    #Which videos the admins have to currently watch respectively
    admin = request.user.username
    admin_obj = Admin_info.objects.get(username = admin)
    vid_key = next(iter(admin_obj.priorityq))
    video = admin_obj.priorityq.get(vid_key)
    return render(request, "webadmin/Showrec.html", {"video" : video})
    
def assign_priority():  #given based on criteria
    
def next_video():   #video the admin has to watch after they finished watching the previous and delete previos from queue
  
def add_video_details(request, v_id):    #add video in admin's queue
    admin_assigned = select_admin() #object
    # admin_json_field_insert_(pq, pk)
    getq = dict(admin_assigned.priorityq)
    p = assign_priority()
    getq[p] = v_id #video id
    di = list(getq.items()) # heapify
    heapq.heapify(di)     # heapify
    di = dict(di)   # heapify
    admin_assigned.size += 1
    admin_assigned.priorityq = di.copy()
    admin_assigned.save()