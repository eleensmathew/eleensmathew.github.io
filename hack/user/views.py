from django.shortcuts import render
# Create your views here.
from django.contrib import messages
from django.views import View
from django.http import JsonResponse
from django.http import HttpResponse
from azure.core.exceptions import ResourceNotFoundError
from azure.core.credentials import AzureKeyCredential
# from azure.ai.formrecognizer import FormRecognizerClient
# import uuid
# from azure.storage.blob import BlockBlobService
from azure.storage.blob import BlobServiceClient
from django.conf import settings
from django.http import (HttpResponse, HttpResponseBadRequest, 
                         HttpResponseForbidden, HttpResponseServerError)
from django.http import JsonResponse
#from django_extensions.management.notebook_extension import run_notebook
from .kernel import *
import cv2
import random
import os
import uuid  
from django.utils.text import slugify
from .models import Storage
from webadmin.views import add_video_details
# from azure.storage.blob import ContentSettings
#class Uploader(View):
    
#     def post(self, request):
#         try:
#             file = request.FILES['file']
#             filename = file.name
#             file_upload_name = str(uuid.uuid4()) + file.name
#             blob_service_client = BlockBlobService(account_name = 'strageforhack36o', account_key='0noTnpz6YAgW4UjuJkM7hD7Glo+S+LAeD/0aKFD53nISV1aw6GAnsx2lLZvPveXjcyCdLQ3tOj+R+AStv6/sRw==')
#             #blob_service_client.create_blob_from_bytes( container_name = 'container-name', blob_name = file_upload_name, blob = file.read())
#             blob_service_client.create_blob_from_bytes( container_name = 'media', blob_name = file_upload_name, blob = file.read(), content_settings = ContentSettings(content_type='video/mp4', content_disposition='inline'))
#             return JsonResponse( { "status": "success", "uploaded_file_name": file_upload_name}, status=201)
        
#         except:
#             messages.error(request,"Please try again")
def Upload(request):
    return render(request, 'upload.html')
         #return render(request,"upload.html")
# def upload_video(request):
#     if request.method == 'POST' and request.FILES['video_file']:
#         video_file = request.FILES['video_file']
        
#         # Save the file to disk (for processing)
#         with open('tmp/video.mp4', 'wb+') as destination:
#             for chunk in video_file.chunks():
#                 destination.write(chunk)

#         # Analyze the video for guns
#         analysis_result = True#analyze_video_for_guns('tmp/video.mp4')
        
#         # If a gun is detected, save the video to Azure Blob Storage
#         if analysis_result['is_gun_detected']:
#             blob_service_client = BlobServiceClient.from_connection_string(settings.AZURE_STORAGE_CONNECTION_STRING)
#             container_client = blob_service_client.get_container_client('video-container')

#             try:
#                 with open('tmp/video.mp4', 'rb') as data:
#                     container_client.upload_blob(name='video.mp4', data=data)
#             except ResourceNotFoundError:
#                 return HttpResponse('Could not find container "video-container"')

#         return HttpResponse('Video analysis complete')
import logging

def upload_video(request):
    if request.method == 'POST':
        
        try:
            video_file = request.FILES['video_file']
        except KeyError:
            print(request.FILES)
            logging.error('No video file found in request')
            return HttpResponseBadRequest('No video file found in request')
        
        # Save the file to disk (for processing)
        if not os.path.exists('tmp'):
            os.makedirs('tmp')
        storage = Storage()
        storage.name  = video_file.name.split('.')[0]
        slugn =storage.name + str(uuid.uuid1())
        slugd = slugify(slugn)
        vid_path = "tmp/" + slugd + ".mp4"
        storage.slug = vid_path
        storage.save()
        prioritynum = 1
        add_video_details(prioritynum, vid_path)
        with open(vid_path, 'wb+') as destination:
            for chunk in video_file.chunks():
                destination.write(chunk)

        # Analyze the video for guns
        #analysis_result = analyze_video_for_guns('tmp/video.mp4')
        analysis_result = {'is_gun_detected': True}
        # If a gun is detected, save the video to Azure Blob Storage
        if analysis_result['is_gun_detected']:
            blob_service_client = BlobServiceClient.from_connection_string(settings.AZURE_STORAGE_CONNECTION_STRING)
            container_client = blob_service_client.get_container_client('media')

            try:
                with open(vid_path, 'rb') as data:
                    container_client.upload_blob(name=vid_path, data=data)
            except ResourceNotFoundError:
                logging.error('Could not find container "video-container"')
                return HttpResponseServerError('Could not find container "video-container"')

        return HttpResponse('Video analysis complete')
    return render(request, 'upload.html')

def delete_image(path):
    os.remove(path)
def extract_images():#(video_file):
    cap = cv2.VideoCapture('/home/eleensmathew/hack36-project/video.mp4')#(video_file)
    images_dir = os.path.join(settings.MEDIA_ROOT, 'extracted_images')
    os.makedirs(images_dir, exist_ok=True)
    frame_indices = sorted(random.sample(range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))), 5))
    for i in frame_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if not ret:
            break

        image_file = os.path.join(images_dir, f"frame_{i}.jpg")
        cv2.imwrite(image_file, frame)
    cap.release()
