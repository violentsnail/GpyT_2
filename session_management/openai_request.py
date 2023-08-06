# openai_request.py
import openai
from datetime import datetime
import json

def openai_request(session_id, model, message):
    with open('config.json') as json_file:
        data = json.load(json_file)
    openai.api_key = data["openai_api_key"]

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": f"You are chatting with a fine-tuned {model} model. You can provide a message or prompt."
            },
            {
                "role": "user",
                "content": message
            }
        ]
    )
    
    return response.choices[0].message['content']