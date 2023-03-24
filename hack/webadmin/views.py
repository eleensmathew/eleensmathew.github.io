from django.shortcuts import render
from .models import Priority, Admin_info
# Create your views here.

#def select_admin(): #Selecting which admin should monitor that video recording
    
# def get_video():    #Which videos the admins have to currently watch respectively
    
# def assign_priority(assigned):  #setting the priority of the new video in selected admin's queue
    
    
# def next_video():   #video the admin has to watch after they finished watching the previous and delete previos from queue
  
#def add_video_details():    #add video in admin's queue
      #create the object having pq and pk of new video
      #pk will be fetched from the cloud storage
      #pq will be calculated based on hash function for assigning priority to the events
    #   admin_assigned = select_admin() #object
    #   priority_val = assign_priority(admin_assigned)
    #   #pk_val = fetched
    #   new_video = Priority.objects.create(pq=priority_val, pk_value=pk_val, admin_associated=admin_assigned)
    #   new_video.save()
