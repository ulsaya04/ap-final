import subprocess
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.generic import TemplateView
from django.conf import settings

from .serializers import *
# Create your views here.
from datetime import datetime
from django.http import JsonResponse
# import pyaudio
import speech_recognition as sr
import io
from pydub import AudioSegment
import os
import tempfile
import pyaudio
import wave
# from pydub import AudioSegment
# import wave
# import os

def capture_audio(request):
    if request.method == 'POST' and request.FILES.get('audio_data'):
        audio_file = request.FILES['audio_data']
        # Process the audio file here, e.g., save it to the server or perform analysis
        
        return JsonResponse({'message': 'Audio captured successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

class CaptureAudio(APIView):
    def speech_to_text(self, audio_file):
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            try:
                audio_text = recognizer.record(source)
                text = recognizer.recognize_google(audio_text, language="en-US")
                return text
            except sr.UnknownValueError:
                return "Google Web Speech API could not understand the audio"
            except sr.RequestError as e:
                return f"Could not request results from Google Web Speech API; {e}"
    
    def convert_to_supported_format(self, audio_file):
        output_file = audio_file.replace('.webm', f'_converted_{int(datetime.now().timestamp())}.wav')  
        command = f'{settings.BASE_DIR}/ffmpeg/bin/ffmpeg.exe -i "{audio_file}" -acodec pcm_s16le -ar 44100 -ac 1 "{output_file}"'
        try:
            subprocess.run(command, shell=True, check=True)
            print("Conversion completed successfully")
            return output_file  # Return the path to the converted audio file
        except subprocess.CalledProcessError as e:
            print("Error during conversion:", e)
            return None  # Return None to indicate failure

    def save_audio(self, file, target_rate=44100, chunk_size=1024):
        save_path = os.path.join(settings.MEDIA_ROOT, 'uploads', file.name +f'{int(datetime.now().timestamp())}' + '.webm')

        with open(save_path, 'wb') as destination:
            for chunk in file.chunks(chunk_size=chunk_size):
                destination.write(chunk)
        
        converted_audio_path = self.convert_to_supported_format(save_path)
        return converted_audio_path
            
        
    def post(self, request):
        if 'audio_data' in request.FILES:
            audio_file = request.FILES['audio_data']
            audio_file_path = self.save_audio(audio_file)
            if audio_file_path:
                text = self.speech_to_text(audio_file_path)
                return Response({'text': text}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Error converting audio'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': 'No audio file provided'}, status=status.HTTP_400_BAD_REQUEST)


class main(TemplateView):
    template_name = 'index.html'



class FromAudio(APIView):
    def save_audio(self, file, target_rate=44100, chunk_size=1024):
        save_path = os.path.join(settings.MEDIA_ROOT, 'uploads', file.name +f'{int(datetime.now().timestamp())}' + '.webm')

        with open(save_path, 'wb') as destination:
            for chunk in file.chunks(chunk_size=chunk_size):
                destination.write(chunk)
        
        return save_path
            
    
    def speech_to_text(self, file):
        recognizer = sr.Recognizer()
        with sr.AudioFile(file) as source:
            try:
                audio_text = recognizer.record(source)
                text = recognizer.recognize_google(audio_text, language="en-US")
                return text
            except sr.UnknownValueError:
                return "Google Web Speech API could not understand the audio"
            except sr.RequestError as e:
                return f"Could not request results from Google Web Speech API; {e}"
    
    def post(self, request):
        if 'audio_data' in request.FILES:
            audio_file = request.FILES['audio_data']
            audio_file_path = self.save_audio(audio_file)
            if audio_file_path:
                text = self.speech_to_text(audio_file_path)
                return Response({'text': text}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Error converting audio'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': 'No audio file provided'}, status=status.HTTP_400_BAD_REQUEST)

