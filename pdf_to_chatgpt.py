import asyncio
from openai import AsyncOpenAI

# Initialize the AsyncOpenAI client
client = AsyncOpenAI(
    api_key="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",
)


async def main():
    # Read the PDF file as binary
    with open(r"C:\Users\Rob\Downloads\534120_2023_SPECIALTY_CAPITAL_LLC_v_SPECIALTY_CAPITAL_LLC_EXHIBIT_S__2.pdf", 'rb') as file:
        pdf_data = file.read()

    # Create the chat completion with the PDF file
    chat_completion = await client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f'Please extract any names, including business names, and points of contact including names, emails, and phone numbers from the following pdf', "file": pdf_data}
        ],
        model="gpt-3.5-turbo",
    )

    # Print the response
    print(chat_completion)
    print(chat_completion.choices[0].message.content)

# Run the main function
asyncio.run(main())
