import openai 
from openai import OpenAI
import os

endpoint = "https://cdong1--azure-proxy-web-app.modal.run"
api_key = "supersecretkey"
deployment_name = "gpt-4o"
client = OpenAI(
    base_url=endpoint,
    api_key=api_key
)

response = client.chat.completions.create(
    model=deployment_name,
    messages=[
        {
            "role": "system",  
            "content": "Talk professionally and be helpful. Make sure to be concise and efficent with answers dont waste tokens. Start with a greeting and generate a trustworthy sounding american name. You will be referred to by this name by the user so make sure to remember it"
        },
        {
            "role": "user",
            "content": "I am a customer looking for help with an issue relating to your product/service."
        }
    ]
)

print(response.choices[0].message.content)