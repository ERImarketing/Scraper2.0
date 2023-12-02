import json
import os
import requests
import time

from dotenv import load_dotenv
from upload_file import upload_file
from create_asssistant import create_assistant
from create_thread import create_thread
from get_steps import get_steps
from send_to_airtable import send_to_airtable


def send_to_gpt(file_path, file_name):

    load_dotenv()
    open_ai_key = os.getenv('OPENAI_API')

    file_upload_id = upload_file(file_name, file_path)
    assistant_id = create_assistant(file_upload_id)
    thread_id, run_id = create_thread(assistant_id, file_upload_id)
    msg_data = get_steps(thread_id, run_id)

    while True:
        if len(msg_data['data']) != 0:
            if msg_data['data'][0]['status'] == 'failed':
                file_upload_id = upload_file(file_name, file_path)
                assistant_id = create_assistant(file_upload_id)
                thread_id, run_id = create_thread(assistant_id, file_upload_id)
                msg_data = get_steps(thread_id, run_id)
            if msg_data['data'][0]['status'] == 'in_progress':
                print(f'Current Status is {msg_data["data"][0]["status"]}')
                time.sleep(20)
                msg_data = get_steps(thread_id, run_id)
            else:
                try:
                    msg_id = msg_data['data'][0]['step_details']['message_creation']['message_id']
                    break
                except:
                    continue
        else:
            msg_data = get_steps(thread_id, run_id)

    url = f"https://api.openai.com/v1/threads/{thread_id}/messages/{msg_id}"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {open_ai_key}',
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
            final_msg_index = final_msg.find('{')
            final_msg = final_msg[final_msg_index:-3].strip()
            final_msg = final_msg.replace('\n', '')
            print(f'Extracted Data: {final_msg}')
            print('------------------')
            final_msg_json = json.loads(final_msg)
            debt_amount = final_msg_json['Debt Amount']
            if debt_amount >= 20000:
                send_to_airtable(final_msg)
        else:
            break


def process_files(directory):
    for file_name in os.listdir(directory):
        # Check if the file is a PDF
        if file_name.endswith(".pdf"):
            file_path = os.path.join(directory, file_name)
            send_to_gpt(file_path, file_name)
