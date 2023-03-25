from django.shortcuts import render
# Create your views here.
from django.contrib import messages
from django.views import View
from django.http import JsonResponse
from django.http import HttpResponse
from azure.core.exceptions import ResourceNotFoundError
from azure.core.credentials import AzureKeyCredential
# from django_extensions.management.notebook_extension import shell_plus
# from azure.ai.formrecognizer import FormRecognizerClient
# import uuid
# from azure.storage.blob import BlockBlobService
from azure.storage.blob import BlobServiceClient
from django.conf import settings
from django.http import (HttpResponse, HttpResponseBadRequest, 
                         HttpResponseForbidden, HttpResponseServerError)
from django.http import JsonResponse
#from django_extensions.management.notebook_extension import run_notebook
#from .kernel import *
import cv2
import random
import os
import uuid  
from django.utils.text import slugify
from .models import Storage#, Scores
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
    tup = get_location(request)
    tup0 = str(tup[0])
    tup1 = str(tup[1])
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
            
        # extract_images(video_file)
        
        storage = Storage()
        storage.name  = video_file.name.split('.')[0]
        slugn =storage.name + str(uuid.uuid1())
        slugd = slugify(slugn)
        # vid_path = "tmp/" + slugd + ".mp4"
        string = "webadmin/"
        s = slugd + ".mp4"
        vid_path = string+ s
        storage.slug = vid_path
        storage.location = tup0 + " " + tup1
        storage.save()
        prioritynum = 1
        add_video_details(prioritynum, s)
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
# def analyze_video_for_guns(video_path):
#     # Create a FormRecognizerClient instance
#     credential = AzureKeyCredential(settings.AZURE_FORM_RECOGNIZER_API_KEY)
#     client = FormRecognizerClient(endpoint=settings.AZURE_FORM_RECOGNIZER_ENDPOINT, credential=credential)

#     # Analyze the video file for gun detection
#     with open(video_path, "rb") as f:
#         poller = client.begin_recognize_video_in_stream(
#             video_stream=f,
#             detect_options={
#                 "include": ["weapons"]
#             },
#             video_content_type="video/mp4"
#         )
#     analysis_result = poller.result()

#     # Return the analysis result
#     return {
#         'is_gun_detected': any([weapon.confidence > 0.5 for weapon in analysis_result.weapons])
#     }

# def delete_image(path):
#     os.remove(path)
def extract_images():#video_file_name):
    # Open the video file
    video_file_name = '/mnt/c/Users/amita/OneDrive/Desktop/django_proj/eleensmathew.github.io/hack/tmp/video.mp4'
    cap = cv2.VideoCapture(video_file_name)#(video_file)

    # name  = video_file_name.split('.')[0]
    # slugn = name + str(uuid.uuid1())
    # slugd = slugify(slugn)
    # vid_folder_name = slugd
    
    # Create a directory to save the extracted images
    images_dir = os.path.join(settings.MEDIA_ROOT, 'extracted_images2')#vid_folder_name)
    os.makedirs(images_dir, exist_ok=True)

    # Extract 5 random images from the video file
    #frame_indices = sorted(random.sample(range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))), 2))
    framecount=0
    f = open('img_paths.txt', 'w+')
    while cap.isOpened() and framecount<5:
        ret, frame=cap.read()
        if not ret:
            break
    # for i in frame_indices:
    #     cap.set(cv2.CAP_PROP_POS_FRAMES, i)
    #     ret, frame = cap.read()
    #     if not ret:
    #         break

        # Save the frame as an image file
        image_file = os.path.join(images_dir, f"frame_{framecount}.jpg")
        framecount+=1
        cv2.imwrite(image_file, frame)
        f.write(image_file + "\n")

    # Release the video file
    cap.release()
    f.close()
    # f = open('img_paths.txt', 'w+')
    # f.write()
    # f.close()

    # Call another function with the extracted images
#extract_images()

# def analyse(request):
#     image_folder_path = '/media'
#     image_paths = [os.path.join(image_folder_path, f) for f in os.listdir(image_folder_path) if f.endswith('.jpg') or f.endswith('.png') or f.endswith('.jpeg')]
#     output = {}#run_notebook('.ipynb', image_paths=image_paths)
#     return output

# def run_jupyter():
#     media_folder = settings.MEDIA_ROOT
    
#     # get list of image paths
#     image_paths = [os.path.join(media_folder, f) for f in os.listdir(media_folder) if f.endswith(('.jpg', '.png', '.jpeg'))]
    
#     # pass image paths to Jupyter notebook
#     shell_plus(line=f'run hello.ipynb {image_paths}')
#     shell_plus(line=f'run hello.ipynb {image_paths}')

#     # return response
#     return JsonResponse({'message': 'Jupyter notebook completed successfully'})

def get_location(request):
    if request.method == 'POST':
        if 'location' in request.POST:
            lat, lng = request.POST['location'].split(',')
            return (lat, lng)
