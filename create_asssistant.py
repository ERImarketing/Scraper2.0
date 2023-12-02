import os
import json
import requests
import time

from dotenv import load_dotenv


def create_assistant(file_upload_id):

    load_dotenv()
    openai_key = os.getenv('OPENAI_API')

    create_assistant_url = "https://api.openai.com/v1/assistants"

    payload = json.dumps({
        "instructions": "Your are a personal assistant.",
        "tools": [
            {
                "type": "retrieval"
            }
        ],
        "model": "gpt-4-1106-preview",
        "file_ids": [
            f"{file_upload_id}"
        ]
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {openai_key}',
        'OpenAI-Beta': 'assistants=v1',
    }

    response = requests.request(
        "POST", create_assistant_url, headers=headers, data=payload)

    assistant_data = json.loads(response.text)

    assistant_id = assistant_data['id']

    print(f"Assistant ID: {assistant_id}")

    return assistant_id
