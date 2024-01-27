import os
import openai


client = openai.OpenAI()
completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a meeting assistant, you will be provided with textual input from a company meeting and you are to provide a meeting transcript with a summary at the end "},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
)

print(completion.choices[0].message)
