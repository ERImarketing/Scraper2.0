import os
import json
import requests

from dotenv import load_dotenv


def send_to_airtable(json_data):

    load_dotenv()
    airtable_api = os.getenv('AIRTABLE_API')

    url = "https://api.airtable.com/v0/appho2OWyOBvn6PPU/tblUbpnS3E0BDL74O"

    payload = json.dumps({
        "records": [
            {
                "fields": {
                    "ChatGPT Response": json_data
                }
            }
        ]
    })
    headers = {
        'Authorization': f'Bearer {airtable_api}',
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
