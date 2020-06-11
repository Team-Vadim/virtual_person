from os import path
from pydub import AudioSegment
import requests
import speech_recognition
import urllib.request
import json

# files
src = "dece9e8301.ogg"  # Путь к файлу, который надо конвертировать
dst = "audios.wav"  # Путь к итоговому файлу

sound = AudioSegment.from_ogg(src)
sound.export(dst, format="wav")
recog = speech_recognition.Recognizer()
sample_audio = speech_recognition.AudioFile('audios.wav')
with sample_audio as audio_file:
    audio_content = recog.record(audio_file)
print('here')
print(recog.recognize_google(audio_content, language='ru'))
