import os
import json
import requests

from dotenv import load_dotenv


def create_thread(assistant_id, file_upload_id):

    load_dotenv()
    openai_key = os.getenv('OPENAI_API')

    url = "https://api.openai.com/v1/threads/runs"

    print(f'Sending Post Request to: {url}')

    payload = json.dumps({
        "assistant_id": f"{assistant_id}",
        "thread": {
            "messages": [
                {
                    "role": "user",
                    "content": f"Read file {file_upload_id}.  Extract the details about both parties involved. The response should contain any names, phone numbers, emails, or addresses listed by either party as well as the total sum of the debt owed. When assigning the key to the debt owed always name the key \"Debt Amount\" and it should always be a top level key value pair, it should never be nested and always returned in a number format. Return the response as a JSON object only, no explanations."
                }
            ]
        }
    })
    headers = {
        'Authorization': f'Bearer {openai_key}',
        'Content-Type': 'application/json',
        'OpenAI-Beta': 'assistants=v1',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    thread_data = json.loads(response.text)

    thread_id = thread_data['thread_id']
    run_id = thread_data['id']

    return thread_id, run_id
