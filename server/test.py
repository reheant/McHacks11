import speech_recognition as sr
import time
from concurrent.futures import ThreadPoolExecutor
import openai
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
         transcript. Return me in JSON, the values that match.
         '''},
        {"role": "user", "content": "Here is the meeting agenda for the meeting: " + meeting_minutes + " here is the transcript"  + transcript}
    ]
)
    
    print(completion.choices[0].message)


def record_audio(start_time, init_rec, source):
    meeting_transcript = ""
    with ThreadPoolExecutor(max_workers=1) as executor:
        while time.time() - start_time < (60*2):
            audio = init_rec.record(source, duration=10)
            future = executor.submit(recognize_audio, audio)
            meeting_transcript += future.result()
            setting_openAI(meeting_transcript, set_meeting_minutes())
            time.sleep(1) 
    return meeting_transcript

init_rec = sr.Recognizer()
with sr.Microphone() as source:
    start_time = time.time()
    transcript = record_audio(start_time, init_rec, source)
    print(transcript)


