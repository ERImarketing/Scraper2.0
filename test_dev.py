import openai
from openai import OpenAI
from pathlib import Path
import base64
import asyncio
from openai import AsyncOpenAI, OpenAI

# Initialize the AsyncOpenAI client
async_client = AsyncOpenAI(
    api_key="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",
)

# Function to encode PDF to base64


# async def encode_pdf_to_base64(file_path):
#     with open(file_path, "rb") as pdf_file:
#         encoded_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')
#     return encoded_pdf


# async def main():
#     # Encode your PDF file
#     encoded_pdf = await encode_pdf_to_base64(r"C:\Users\Rob\Downloads\534120_2023_SPECIALTY_CAPITAL_LLC_v_SPECIALTY_CAPITAL_LLC_EXHIBIT_S__2.pdf")

#     # Create the chat completion with the encoded PDF
#     chat_completion = await client.chat.completions.create(
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": f'Please extract the any names, including business names, and points of contact including names, emails, and phone numbers from the following pdf {encoded_pdf}'}
#         ],
#         model="gpt-4-1106-preview",
#     )

#     # Print the response
#     print(chat_completion)
#     print(chat_completion.choices[0].message.content)

# Run the main function
# asyncio.run(main())


file_response = async_client.files.create(
    file=Path(r"C:\Users\Rob\Downloads\534120_2023_SPECIALTY_CAPITAL_LLC_v_SPECIALTY_CAPITAL_LLC_EXHIBIT_S__2.pdf"),
    purpose="fine-tune",
)

print(file_response)


# Set your API key
client = OpenAI(
    api_key="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",
)
# Retrieve a list of file objects
file_list = client.files.list()

# Print the list of files
for file in file_list.data:
    print(file.id, file.filename, file.purpose)
