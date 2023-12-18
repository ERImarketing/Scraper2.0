import json
import os
import requests
import time

from dotenv import load_dotenv


def get_message(thread_id, msg_id):
    load_dotenv()
    OPEN_API = os.getenv('OPEN_API')

    url = f"https://api.openai.com/v1/threads/{thread_id}/messages/{msg_id}"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OPEN_API}',
        'OpenAI-Beta': 'assistants=v1',
    }

    final_msg = ''

    while True:
        if final_msg == '':
            time.sleep(10)
            response = requests.request(
                "GET", url, headers=headers)
            final_msg_data = json.loads(response.text)
            final_msg = final_msg_data['content'][0]['text']['value']
            print(f'Extracted Data: {final_msg}')
            print('------------------')
            return final_msg
        else:
            break
