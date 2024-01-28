import speech_recognition as sr
import time
from concurrent.futures import ThreadPoolExecutor
import openai
import numpy as np
import wave
import os
client = openai.OpenAI()

def set_meeting_minutes():
    meeting_minutes = '''
Meeting Agenda

Date: [Insert Date]
Time: [Insert Time]
Duration: 30 minutes
Location: [Insert Location/Video Conference Link]
Attendees: [List Attendees]

Opening

1. Welcome & Introductions (5 minutes)
2. Review of Agenda (2 minutes)
3.Business Overview

4. Brief recap of last meeting's action items (3 minutes)
5. Current performance snapshot (financials, key metrics) (5 minutes)
6. Project Updates

7. Update on Project  X (3 minutes)
8. Discussion on challenges and solutions (5 minutes)
9. New Business

10. Introduction of new initiative/strategy (5 minutes)
11. Open floor for suggestions and ideas (2 minutes)
12. Closing
13. Confirmation of next meeting date and objectives (2 minutes)
'''
    return meeting_minutes

def recognize_audio(audio):
    try:
        print("Recognizing...")
        text = init_rec.recognize_google(audio, language='en-IN', show_all=True)
        partial_output = text['alternative'][0]['transcript']
        print(partial_output)
        return partial_output
    except sr.UnknownValueError:
        print("Error recognizing audio")
        return ""
    except sr.RequestError:
        print("Broken pipe error but we gonna ignore it cuz i dont got $$$")
        return ""


def setting_openAI(transcript, meeting_minutes):
    
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": '''You are a meeting assistant, compare the different points in the meeting agenda to the points discussed in the 
         transcript. Return me in JSON, the values that match. Respond with true or false for each value.
         '''},
        {"role": "user", "content": "Here is the meeting agenda for the meeting: " + meeting_minutes + " here is the transcript"  + transcript}
    ]
)
    
    print(completion.choices[0].message)
def save_wav(filename, audio_data):
    # Assuming audio_data is a numpy array with dtype=np.int16
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)  # Mono audio
        wf.setsampwidth(2)  # 16-bit audio
        wf.setframerate(44100)  # Adjust according to your audio settings
        wf.writeframes(audio_data.tobytes())

def record_audio(start_time, init_rec, source):
    meeting_transcript = ""
    audio_chunks = []
    with ThreadPoolExecutor(max_workers=1) as executor:
        while time.time() - start_time < (30):
            audio = init_rec.record(source, duration=10)
            future = executor.submit(recognize_audio, audio)
            meeting_transcript += future.result()
             # Check if the audio array is one-dimensional
            if audio.ndim == 1:
                audio = audio.reshape(-1, 1)  # Convert to a column vector
            audio_chunks.append(audio)
            setting_openAI(meeting_transcript, set_meeting_minutes())
            time.sleep(1) 
    combined_audio = np.concatenate(audio_chunks, axis=0)
    output_filename = os.path.join("audio", "transcipt.wav")
    save_wav(output_filename, combined_audio)
    return meeting_transcript
def callback(indata, frames, time, status):
    if status:
        print(status, flush=True)
    wave_file.writeframes(indata.copy())
def record():

init_rec = sr.Recognizer()
with sr.Microphone() as source:
    start_time = time.time()
    transcript = record_audio(start_time, init_rec, source)
    print(transcript)


