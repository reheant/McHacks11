import speech_recognition as sr
import openai
import time

client = openai.OpenAI()
init_rec = sr.Recognizer()
print("Let's speak!!")
meeting_transcript = ""
start_time = time.time()
with sr.Microphone() as source:
    while time.time() - start_time < (60*3):

        try: 
            audio = init_rec.record(source, duration=10)
            print("recognizing......")
            text = init_rec.recognize_google(audio, language = 'en-IN', show_all = True )
            partial_output = text['alternative'][0]['transcript']
            print(partial_output)

            meeting_transcript += partial_output
            time.sleep(1) 
        except sr.UnknownValueError:
            print("error with this part")
        

    
print(meeting_transcript)
#         completion = client.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": "You are a meeting assistant, you will be provided with textual input from a company meeting and you are to provide a meeting transcript with a summary at the end "},
#     {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
#   ]
# )
        
#         print(completion.choices[0].message)





