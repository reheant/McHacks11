import speech_recognition as sr
import time
from concurrent.futures import ThreadPoolExecutor
import openai
client = openai.OpenAI()

def set_meeting_minutes():
    meeting_minutes = '''
Meeting Minutes
Date: January 27, 2024
Time: 10:00 AM - 11:30 AM
Location: Conference Room B, Vertex Solutions Headquarters

Attendees:

Samantha Green (CEO)
Alex Chen (CFO)
Emily Johnson (Head of Marketing)
Michael Smith (Head of Product Development)
Lisa Ray (HR Manager)
Absent:

Rahul Gupta (CTO) - On business travel
1. Opening
The meeting was called to order by Samantha Green at 10:05 AM. Samantha welcomed everyone and emphasized the importance of aligning the company's strategies for the upcoming quarter.

2. Approval of Minutes
Minutes from the previous meeting held on December 20, 2023, were circulated and approved.

3. Financial Update (Alex Chen)
Alex presented the financial summary for Q4 2023. Revenue exceeded projections by 8%, primarily due to the successful launch of the new line of productivity software.
Discussed the budget allocation for Q1 2024, with a focus on increasing the R&D budget by 15%.
Proposed a review of current investment portfolios, suggesting a reallocation towards more sustainable and green technologies.
4. Marketing Initiatives (Emily Johnson)
Emily introduced the new marketing campaign "TechForward," aimed at promoting the company's commitment to innovation and sustainability.
Discussed the results of the recent market survey, indicating a strong market presence but a need for improved customer support.
Proposed a partnership with influencers in the tech industry to boost the upcoming product launch.
5. Product Development Update (Michael Smith)
Michael provided an update on the development of the AI-driven analytics tool, highlighting the successful integration of real-time data processing features.
Discussed challenges in the current testing phase, particularly in data security and user privacy.
Proposed hiring additional AI specialists to expedite the project's completion.
6. HR Updates (Lisa Ray)
Lisa presented the quarterly HR report, noting a 95% employee satisfaction rate.
Discussed the upcoming leadership training program and the introduction of a new wellness initiative.
Addressed the need to revise the remote work policy to accommodate hybrid work models better.
7. Miscellaneous Issues
Samantha reminded the team about the upcoming annual shareholders' meeting.
Alex suggested scheduling a financial audit in March.
Emily requested additional resources for the marketing team to ensure the success of the "TechForward" campaign.
8. Closing
Samantha thanked everyone for their contributions and adjourned the meeting at 11:20 AM. The next meeting was scheduled for February 24, 2024.

Minutes prepared by: Jessica Parker (Executive Assistant)
Minutes approved by: Samantha Green (CEO)

[Distribution: All Attendees, Company Board Members]
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


def setting_openAI():
    
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": '''You are a meeting assistant, you will be provided with meeting minutes for a company meeting, you will also be provided with 
         
         '''},
        {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
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
            time.sleep(1)  
    return meeting_transcript

init_rec = sr.Recognizer()
with sr.Microphone() as source:
    start_time = time.time()
    transcript = record_audio(start_time, init_rec, source)
    print(transcript)


