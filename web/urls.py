from django.urls import path
from .views import main, CaptureAudio, FromAudio

urlpatterns = [
    path('', main.as_view(), name='main'),
    path('capture-audio/', CaptureAudio.as_view(), name='capture-audio'),
    path('getaudio/', FromAudio.as_view(), name='from-audio'),
]