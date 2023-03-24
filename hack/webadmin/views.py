from django.shortcuts import render
from .models import Priority, Admin_info
import heapq
# Create your views here.

def select_admin(): #Selecting which admin should monitor that video recording
    
def get_video(request):    #Which videos the admins have to currently watch respectively
    vid = Priority.objects.filter(pq=1, admin_associated=request.user)
    
    
def assign_priority():  #given based on criteria
    
def next_video():   #video the admin has to watch after they finished watching the previous and delete previos from queue
  
def add_video_details():    #add video in admin's queue
    admin_assigned = select_admin() #object
    # admin_json_field_insert_(pq, pk)
    getq = admin_assigned.priorityq
    pq = assign_priority()
    getq.append({})
    heapq.heapify(getq)     # heapify
    admin_assigned.save()
    # proirity++