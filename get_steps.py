import os
import json
import requests
import time

from dotenv import load_dotenv


def get_steps(thread_id, run_id):

    load_dotenv()
    openai_key = os.getenv('OPENAI_API')

    url = f"https://api.openai.com/v1/threads/{thread_id}/runs/{run_id}/steps"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {openai_key}',
        'OpenAI-Beta': 'assistants=v1',
    }

    time.sleep(20)

    print(f'Sending Get Request to: {url}')

    response = requests.request("GET", url, headers=headers)

    msg_data = json.loads(response.text)

    return msg_data
