import speech_recognition as sr
import time
from concurrent.futures import ThreadPoolExecutor

import openai
import numpy as np
import wave
import os, json
client = openai.OpenAI()
init_rec = sr.Recognizer()
def set_meeting_minutes(input = ""):
    meeting_minutes = input
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
    
    message = completion.choices[0].message.content
    with open('meeting_analysis_output.txt', 'a') as file:
        file.write(message + '\n')


def record_audio(start_time, init_rec, source):
    meeting_transcript = ""
    with ThreadPoolExecutor(max_workers=1) as executor:
        while time.time() - start_time < (30):
            audio = init_rec.record(source, duration=10)
            future = executor.submit(recognize_audio, audio)
            meeting_transcript += future.result()
            setting_openAI(meeting_transcript, set_meeting_minutes())
            time.sleep(1) 
    return meeting_transcript


def final_record(agenda):
    set_meeting_minutes(agenda)
    with sr.Microphone() as source:
        start_time = time.time()
        transcript = record_audio(start_time, init_rec, source)
        print(transcript)


def read_json_objects_from_file():
    file_path = "./meeting_analysis_output.txt"
    with open(file_path, 'r') as file:
        file_content = file.read().strip()
        json_objects = []
        brace_level = 0
        current_object = ''

        for char in file_content:
            if char == '{':
                brace_level += 1
                current_object += char
            elif char == '}':
                brace_level -= 1
                current_object += char
                if brace_level == 0:
                    try:
                        json_objects.append(json.loads(current_object))
                    except json.JSONDecodeError as e:
                        print("Error")
                    current_object = ''
            else:
                if brace_level > 0:
                    current_object += char

        return json_objects

#final_record()