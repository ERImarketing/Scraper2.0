import json
import requests
import time
import os

from dotenv import load_dotenv
from upload_file import upload_file
from create_asssistant import create_assistant
from create_thread import create_thread
from get_steps import get_steps
from retrieve_message import get_message


def send_to_gpt(file_path, file_name):
    load_dotenv()
    OPEN_API = os.getenv('OPEN_API')

    file_upload_id = upload_file(file_name, file_path)
    assistant_id = create_assistant(file_upload_id)
    thread_id, run_id = create_thread(assistant_id, file_upload_id)
    msg_data = get_steps(thread_id, run_id)

    while True:
        if msg_data['data'][0]['status'] == 'failed':
            file_upload_id = upload_file(file_name, file_path)
            assistant_id = create_assistant(file_upload_id)
            thread_id, run_id = create_thread(assistant_id, file_upload_id)
            msg_data = get_steps(thread_id, run_id)
        if msg_data['data'][0]['status'] == 'in_progress':
            print(f'Current Status is {msg_data["data"][0]["status"]}')
            msg_data = get_steps(thread_id, run_id)
        else:
            msg_id = msg_data['data'][0]['step_details']['message_creation']['message_id']
            break

    final_msg = get_message(thread_id, msg_id)

    return final_msg


def process_files(directory):
    for file_name in os.listdir(directory):
        # Check if the file is a PDF
        if file_name.endswith(".pdf"):
            file_path = os.path.join(directory, file_name)
            send_to_gpt(file_path, file_name)


# For Testing
# process_files('.\\tmp\\pdf')
