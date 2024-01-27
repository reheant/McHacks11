import speech_recognition as sr
import pyaudio

init_rec = sr.Recognizer()
print("Let's speak!!")
with sr.Microphone() as source:
    audio = init_rec.record(source, duration=3)
    print("recognizing......")
    text = init_rec.recognize_google(audio, language = 'en-IN', show_all = True )
    partial_output = text['alternative'][0]['transcript']
    print(partial_output)
