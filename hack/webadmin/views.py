from django.shortcuts import render
from .models import PriorityQueue, Admin_info
# Create your views here.

def select_admin(): #Selecting which admin should monitor that video recording
    admin_select = Admin_info.objects.values_list('priority.total_values()', 'username') #or use lists(...all)
    min_tuple = min(admin_select, key=lambda tup: tup[0])
    return min_tuple[1]
    
def get_video(request):    #Which videos the admins have to currently watch respectively
    admin = request.user.username
    admin_obj = Admin_info.objects.get(username = admin)
    #if admin_obj.total_values() == 0:
    video = admin_obj.priority.pop()
    videonext = admin_obj.priority.peek()
    return render(request, "webadmin/Showrec.html", {"video" : video,
                                                     "videonext" : videonext
                                                     })
    
def assign_priority():  #given based on criteria
    
    
def add_video_details(request, v_id):    #add video in admin's queue
    admin_assigned = Admin_info.objects.get(username = select_admin()) #object
    p = assign_priority()
    pobj = admin_assigned.priority
    if pobj.total_values() == 0:
        pobj = PriorityQueue()
        pobj.push(p, v_id)
        admin_assigned.priority = pobj
    else:
        pobj.push(p, v_id)
    admin_assigned.save()