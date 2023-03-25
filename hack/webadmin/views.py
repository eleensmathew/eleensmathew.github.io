from django.shortcuts import render, redirect
from .models import PriorityQueue, Admin_info, CustomUser
from .forms import LogInForm
from django.contrib.auth.decorators import login_required
from django.db.models import Min
from django.contrib.auth import login as django_login, authenticate, logout as django_logout
from django.urls import reverse
from azure.storage.blob import BlobServiceClient
from azure.storage.blob import BlobClient, BlobBlock
from django.http import HttpResponse
from django.conf import settings


def stream_video(request):
    # Get the connection string and container name from settings
    connection_string = settings.AZURE_STORAGE_CONNECTION_STRING
    container_name = 'media'

    # Create a BlobServiceClient object using the connection string
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    
    # Create a BlobClient object for the video file
    li = get_video(request)
    video = li[0]
    videonext = li[1]
    # print(video)
    blob_name="webadmin/" + video
    blob_client = blob_service_client.get_blob_client(container_name, blob_name)
    
    download_stream = blob_client.download_blob()
    content_type = download_stream.read

    # Set the response headers for video streaming
    # content_type = blob_client.get_blob_properties().content_settings.content_type
    response = HttpResponse(content_type=content_type)

    response['Content-Disposition'] = f'attachment; filename="{blob_name}"'
    # response['Cache-Control'] = 'no-cache'
    # response['X-Accel-Buffering'] = 'no'

    # Stream the video content
    # response.streaming_content = blob_client.download_blob().content_as_bytes()
    response.write(download_stream.readall())
    # Render the template
    # print(video)
    return render(request, "webadmin/Showrec.html", {"video" : video,
                                                     "videonext" : videonext
                                                     })
    # return response

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

@login_required    
def get_video(request):    #Which videos the admins have to currently watch respectively
    adm = request.user.id
    admin_obj = Admin_info.objects.get(user_id = adm)
    if admin_obj.priority.total_values() == 0:
        video = "."
    else:
        video = admin_obj.priority.peek()
    if admin_obj.priority.total_values() == 0:
        videonext = "."
    else:
        videonext = admin_obj.priority.peek()
    return [video,videonext]
    
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

def login(request):
    error = False
    if request.user.is_authenticated:
        return redirect('webadmin:stream_video')
    if request.method == "POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email=email, password=password)
            if user:
                django_login(request)  
                return redirect('webadmin:stream_video')
            else:
                error = True
    else:
        form = LogInForm()

    return render(request, 'webadmin/login.html', {'form': form, 'error': error})


def logout(request):
    django_logout(request)
    return redirect(reverse('webadmin:login'))
  
