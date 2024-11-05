# pip install groq

import os
from apikey import groq_apikey
# hacemos que pueda leerse en nuestro programa
os.environ['GROQ_API_KEY']= groq_apikey

import os
from groq import Groq

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Explica la importancia de modelos de lenguaje rapidos",
        }
    ],
    model="llama3-8b-8192",
)

print(chat_completion.choices[0].message.content)

