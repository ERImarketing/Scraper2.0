import json
import requests
import time

upload_files_url = "https://api.openai.com/v1/files"

payload = {'purpose': 'assistants'}
files = [
    ('file', ('137460_2023_CHARGE_UP_CAPITAL_LLC_v_SIDIKYS_LLC_et_al_SUMMONS___COMPLAINT_1.pdf', open(
        r'C:/Users/Rob/Desktop/NyGovScraper/tmp/pdf/137460_2023_CHARGE_UP_CAPITAL_LLC_v_SIDIKYS_LLC_et_al_SUMMONS___COMPLAINT_1.pdf', 'rb'), 'application/pdf'))
]
headers = {
    'Authorization': 'Bearer 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',
}

file_upload_response = requests.request(
    "POST", upload_files_url, headers=headers, data=payload, files=files)

file_data = json.loads(file_upload_response.text)

file_upload_id = file_data['id']

print(file_upload_id)

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
    'Authorization': 'Bearer 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',
    'OpenAI-Beta': 'assistants=v1',
}

response = requests.request(
    "POST", create_assistant_url, headers=headers, data=payload)

assistant_data = json.loads(response.text)

assistant_id = assistant_data['id']

print(assistant_id)


url = "https://api.openai.com/v1/threads/runs"

payload = json.dumps({
    "assistant_id": f"{assistant_id}",
    "thread": {
        "messages": [
            {
                "role": "user",
                "content": f"Read file {file_upload_id}.  Extract the details about both parties involved. The response should contain any names, phone numbers, emails, or addresses listed by either party. Return the response as a JSON object."
            }
        ]
    }
})
headers = {
    'Authorization': 'Bearer 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',
    'Content-Type': 'application/json',
    'OpenAI-Beta': 'assistants=v1',
}

response = requests.request("POST", url, headers=headers, data=payload)

thread_data = json.loads(response.text)

thread_id = thread_data['thread_id']
run_id = thread_data['id']

print(response.text)


url = f"https://api.openai.com/v1/threads/{thread_id}/runs/{run_id}/steps"

print(url)

payload = {}
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer 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',
    'OpenAI-Beta': 'assistants=v1',
}

time.sleep(20)

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

msg_data = json.loads(response.text)
msg_id = msg_data['data'][0]['step_details']['message_creation']['message_id']


url = f"https://api.openai.com/v1/threads/{thread_id}/messages/{msg_id}"
print(url)

payload = {}
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer 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',
    'OpenAI-Beta': 'assistants=v1',
}

final_msg = ''

while True:
    if final_msg == '':
        time.sleep(10)
        response = requests.request("GET", url, headers=headers, data=payload)
        final_msg_data = json.loads(response.text)
        final_msg = final_msg_data['content'][0]['text']['value']
        print(final_msg)
        print('------------------')
    else:
        break
