from django.shortcuts import render
from .models import PriorityQueue, Admin_info
from django.db.models import Min
# Create your views here.

def select_admin(): #Selecting which admin should monitor that video recording
    admin_select = list(Admin_info.objects.all()) 
    min_val = int(1000)
    sel = admin_select[0]
    for ad in admin_select:
        count = int(ad.priority.total_values())
        if count < min_val:
            sel = ad
            min_val = count
    return sel.user.id
    
def get_video(request):    #Which videos the admins have to currently watch respectively
    admin = request.user.id
    admin_obj = Admin_info.objects.get(user_id = admin)
    #if admin_obj.total_values() == 0:
    video = admin_obj.priority.pop()
    videonext = admin_obj.priority.peek()
    return render(request, "webadmin/Showrec.html", {"video" : video,
                                                     "videonext" : videonext
                                                     })
    
def add_video_details(p, v_id):    #add video in admin's queue
    ad = select_admin()
    admin_assigned = Admin_info.objects.get(user_id = ad) #object
    # print(select_admin())
    pobj = admin_assigned.priority
    if pobj.total_values() == 0:
        pobj = PriorityQueue()
        pobj.push(p, v_id)
        admin_assigned.priority = pobj
    else:
        pobj.push(p, v_id)
    admin_assigned.save()