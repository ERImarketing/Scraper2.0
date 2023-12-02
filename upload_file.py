import os
import json
import requests

from dotenv import load_dotenv


def upload_file(file_name, file_path):

    load_dotenv()
    openai_key = os.getenv('OPENAI_API')

    upload_files_url = "https://api.openai.com/v1/files"

    payload = {'purpose': 'assistants'}
    files = [
        ('file', (f'{file_name}', open(
            file_path, 'rb'), 'application/pdf'))
    ]
    headers = {
        'Authorization': f'Bearer {openai_key}',
    }

    file_upload_response = requests.request(
        "POST", upload_files_url, headers=headers, data=payload, files=files)

    file_data = json.loads(file_upload_response.text)

    file_upload_id = file_data['id']

    print(f'File ID: {file_upload_id}')
    return file_upload_id
