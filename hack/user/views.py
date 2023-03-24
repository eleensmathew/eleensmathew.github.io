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
def upload_video(request):
    if request.method == 'POST' and request.FILES['video_file']:
        video_file = request.FILES['video_file']
        with open('tmp/video.mp4', 'wb+') as destination:
            for chunk in video_file.chunks():
                destination.write(chunk)
        analysis_result = analyze_video_for_guns('tmp/video.mp4')
        if analysis_result['is_gun_detected']:
            blob_service_client = BlobServiceClient.from_connection_string(settings.AZURE_STORAGE_CONNECTION_STRING)
            container_client = blob_service_client.get_container_client('video-container')

            try:
                with open('tmp/video.mp4', 'rb') as data:
                    container_client.upload_blob(name='video.mp4', data=data)
            except ResourceNotFoundError:
                return HttpResponse('Could not find container "video-container"')

        return HttpResponse('Video analysis complete')

    return render(request, 'upload.html')
def analyze_video_for_guns(video_path):
    pass