import os
import openai


client = openai.OpenAI()
openai.api_key="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"
completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
)

print(completion.choices[0].message)
