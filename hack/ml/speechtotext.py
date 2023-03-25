from pocketsphinx import AudioFile
slurwords=[]
def slurdetector(phrase):
    array=phrase.split(" ")
    score=0
    for word in array:
        if word in slurwords:
            score=score+1
    return score

# audio = AudioFile(r"C:\Users\Acer\Downloads\screams\test_EN2002a_2020_2030_pkxxx_4_2.wav")
# for phrase in audio:
#     print(phrase)
#     print(slurdetector(str(phrase)))
# files after part 2
import requests
import time
API_KEY_ASSEMBLYAI='1495d351757048f78629c0402e32f559'
filename = "Natural Language Processing Short.m4a"
upload_endpoint = 'https://api.assemblyai.com/v2/upload'
transcript_endpoint = 'https://api.assemblyai.com/v2/transcript'

headers_auth_only = {'authorization': API_KEY_ASSEMBLYAI}

headers = {
    "authorization": API_KEY_ASSEMBLYAI,
    "content-type": "application/json"
}

CHUNK_SIZE = 5_242_880  # 5MB


def upload(filename):
    def read_file(filename):
        with open(filename, 'rb') as f:
            while True:
                data = f.read(CHUNK_SIZE)
                if not data:
                    break
                yield data

    upload_response = requests.post(upload_endpoint, headers=headers_auth_only, data=read_file(filename))
    return upload_response.json()['upload_url']


def transcribe(audio_url):
    transcript_request = {
        'audio_url': audio_url
    }

    transcript_response = requests.post(transcript_endpoint, json=transcript_request, headers=headers)
    return transcript_response.json()['id']

        
def poll(transcript_id):
    polling_endpoint = transcript_endpoint + '/' + transcript_id
    polling_response = requests.get(polling_endpoint, headers=headers)
    return polling_response.json()


def get_transcription_result_url(url):
    transcribe_id = transcribe(url)
    while True:
        data = poll(transcribe_id)
        if data['status'] == 'completed':
            return data, None
        elif data['status'] == 'error':
            return data, data['error']
            
        print("waiting for 10 seconds")
        time.sleep(10)
        
        
def save_transcript(url, title):
    data, error = get_transcription_result_url(url)
    
    if data:
        print(data['text'])
        print(slurdetector(str(data['text'])))
    elif error:
        print("Error!!!", error)
filename = r"C:\Users\Acer\Downloads\screams\test_EN2002a_2020_2030_pkxxx_4_2.wav"
audio_url = upload(filename)

save_transcript(audio_url, 'file_title')
