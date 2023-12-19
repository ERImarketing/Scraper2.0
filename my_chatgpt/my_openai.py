import csv
from datetime import datetime
import json
import os
import time

from dotenv import load_dotenv
from openai import OpenAI

# Workflow:
# 1. Upload files to OpenAI
# 2. Create an assistant with access to the previously uploaded files
# 3. Create a thread with the assistant
# 4. Send a message to the thread
# 5. Run the thread
# 6. Process the response
# 7. Repeat steps 4-6 until the thread is complete
# 8. Delete the assistant
# 9. Delete the files


def create_assistant(client, file_ids):
    client = OpenAI(
        api_key=os.getenv('OPENAI_API'),
    )

    my_assistant = client.beta.assistants.create(
        #         instructions="""
        #            You have uploaded files as input data to the assistant.

        #             Use the following step-by-step instructions to respond to user inputs:

        #             Step 1: Read all accessible files
        #             Step 2: Extract Plaintiff(s) data
        #                 Step 2.1: Extract Plaintiff’(s) Balance Owed data (data type: float or "unavailable" if not present)
        #             Step 3: Extract Defendant(s) data
        #                 Step 3.1: From the Defendant(s), extract the first full name that is not a business; this data will be used to save first and last names (data type: string or "unavailable" if not present)
        #                 Step 3.2: Extract Defendant’(s) Phone Numbers data (data type: string, combine multiple numbers into a CSV list or "unavailable" if not present)
        #                 Step 3.3: Extract Defendant’(s) Email Addresses data (data type: string, combine multiple emails into a CSV list or "unavailable" if not present)
        #                 Step 3.4: Extract Defendant’(s) Address’(s) data as a single string with the entire address in it (data type: string or "unavailable" if not present)
        #                 Step 3.5: Create a CSV list of the companies sued (data type: string or "unavailable" if not present)
        #             Step 4: Extract Court County data (data type: string or "unavailable" if not present)
        #             Step 5: Convert Balance value to a float number with two decimals
        #             Step 6: Please ensure that you follow these instructions precisely to generate the JSON object as described above. If any data is unavailable in the input, save it as "unavailable" as specified. Convert the data to a JSON object with the following key-value pairs. :

        #             {
        #                 “Creditor”: Plaintiff(s) data (data type: string or "unavailable" if not present),
        #                 “Balance”: Plaintiff’(s) Balance Owed data (data type: float or "unavailable" if not present),
        #                 “Companies Sued”: CSV list of companies sued (data type: string or "unavailable" if not present),
        #                 “First Name”: First Name Data Extracted data (data type: string or "unavailable" if not present),
        #                 “Last Name”: Last Name Data Extracted data (data type: string or "unavailable" if not present),
        #                 “Phone Number”: Defendant’(s) Phone Numbers data (data type: string, combine multiple numbers into a CSV list or "unavailable" if not present),
        #                 “Email”: Defendant’(s) Email Addresses data (data type: string, combine multiple emails into a CSV list or "unavailable" if not present),
        #                 “Address”: Defendant’(s) Address’(s) data (data type: string or "unavailable" if not present),
        #                 “County”: Court County data (data type: string or "unavailable" if not present),
        #                 "Notes": Any additional notes about the file (data type: string or "unavailable" if not present)
        #             }

        # """,
        # instructions="""
        #   **Read all accessible files.**

        #     **Primary Objective:**
        #     - **Always return a JSON object in the response containing the extracted data with all of the key value pairs. **

        #     **File Utilization:**
        #     - **Use all available files to extract the required data as accurately and completely as possible.**

        #     **Triple-Check Protocol:**
        #     - **Ensure thorough verification at three stages:**
        #     1. **Initial Extraction:** Verify the completeness of data during the first extraction from files.
        #     2. **Post-Processing Review:** Recheck the data after any processing or conversion.
        #     3. **Pre-Submission Confirmation:** Confirm the accuracy and completeness of all data before finalizing the JSON object.

        #     **Extract data from Summons:**
        #     - **Plaintiff(s) and Defendant(s) Names:**
        #     - **Plaintiff(s):** Extract Plaintiff listed from Summons (data type: string or "unavailable" if not present). Delete, disregard, or ignore any data labeled "Attorney for Plaintiff."
        #     - **Defendant(s):** Extract Defendants listed from Summons (data type: string or "unavailable" if not present).
        #     - **Primary Defendant:** Extract the first name from listed Defendants that is not a business name, that is the primary defendant (data type: string or "unavailable" if not present).
        #     - **Note:** If there is only one Defendant listed, that is the primary Defendant.

        #     **Extract data from Exhibit files (if available):**
        #     1. **Plaintiff(s) Data:**
        #     - **Balance Owed:** (data type: float or "unavailable" if not present).
        #     2. **Defendant(s) Data:**
        #     - **Note:** Extract the following data for Defendant(s) as the primary source of data if available. If not available, attempt to extract the data from the Summons.
        #     - **First Personal Name (non-business):** (data type: string or "unavailable" if not present).
        #     - **Phone Numbers:** (data type: string, CSV list or "unavailable" if not present).
        #     - **Email Addresses:** (data type: string, CSV list or "unavailable" if not present).
        #     - **Address:** (data type: string or "unavailable" if not present).
        #     - **Note:** The address can almost always be found in the Summons.
        #     - **Companies Sued:** (data type: string, CSV list). Include all defendants in this list, even if it's the only data available about them.
        #     3. **Court County Data:** (data type: string or "unavailable" if not present).
        #     4. **Case Number:** (data type: string or "unavailable" if not present). This is the court ID for example "######/YEAR aka 536793/2023" or "E#######".

        #     **Data Processing Instructions:**
        #     - **Convert Balance value to a float number with two decimal places.**
        #     - **Disregard any data labeled "Attorney for Plaintiff."**


        #     **Note:** Make sure to triple-check data before proceeding to the next step.

        #     **Generate JSON object with key-value pairs:**
        #     - **Note:** Always generate the JSON object with these keys.
        #     - **Creditor:** Plaintiff(s) data (only the name). Exclude "Attorney for Plaintiff" information.
        #     - **Balance:** Plaintiff’s Balance Owed data (if available),
        #     - **Companies Sued:** Ensure to include all defendants in this CSV list, regardless of other available data.
        #     - **First Name:** Extracted First Name of Defendant,
        #     - **Last Name:** Extracted Last Name of Defendant,
        #     - **Phone Number:** Defendant’s Phone Numbers,
        #     - **Email:** Defendant’s Email Addresses,
        #     - **Address:** Defendant’s Address,
        #     - **County:** Court County data,
        #     - **Case Number:** Case Number data,
        #     - **Notes:** Always include a brief summary about the case.

        # """,
        # instructions="""
        #   **Read all accessible files.**

        #     **Primary Objective:**
        #     - **Always return a JSON object in the response containing the extracted data with all the key value pairs. **

        #     **File Utilization:**
        #     - **Use all available files to extract the required data as accurately and completely as possible.**

        #     **Triple-Check Protocol:**
        #     - **Ensure thorough verification at three stages:**
        #     1. **Initial Extraction:** Verify the completeness of data during the first extraction from files.
        #     2. **Post-Processing Review:** Recheck the data after any processing or conversion.
        #     3. **Pre-Submission Confirmation:** Confirm the accuracy and completeness of all data before finalizing the JSON object.

        #     **Extract data from Summons:**
        #     - **Plaintiff(s) and Defendant(s) Names:**
        #     - **Plaintiff(s):** Extract Plaintiff listed from Summons (data type: string or "unavailable" if not present). Delete, disregard, or ignore any data that corresponds to "Attorney for Plaintiff."
        #     - **Defendant(s):** Extract Defendants listed from Summons (data type: string or "unavailable" if not present).
        #     - **Primary Defendant:** Extract the first name from listed Defendants that is not a business name, that is the primary defendant (data type: string or "unavailable" if not present).
        #     - **Address:** Extract any addresses present from listed with Defendants (data type: string, CSV list or "unavailable" if not present).

        #     - **Note:** If there is only one Defendant listed, that is the primary Defendant.

        #     **Extract data from Exhibit files (if available):**
        #     1. **Plaintiff(s) Data:**
        #     - **Balance Owed:** (data type: float or "unavailable" if not present).
        #     2. **Defendant(s) Data:**
        #     - **Note:** Extract the following data for Defendant(s) as the primary source of data if available. If not available, attempt to extract the data from the Summons.
        #     - **First Personal Name (non-business):** (data type: string or "unavailable" if not present).
        #     - **Phone Numbers:** (data type: string, CSV list or "unavailable" if not present).
        #     - **Email Addresses:** (data type: string, CSV list or "unavailable" if not present).
        #     - **Note:** The address can almost always be found in the Summons.
        #     - **Companies Sued:** (data type: string, CSV list). Include all defendants in this list, even if it's the only data available about them.
        #     3. **Court County Data:** (data type: string or "unavailable" if not present).
        #     4. **Case Number:** (data type: string or "unavailable" if not present). This is the court ID for example "######/YEAR aka 536793/2023" or "E#######".

        #     **Data Processing Instructions:**
        #     - **Convert Balance value to a float number with two decimal places.**
        #     - **Disregard any data labeled "Attorney for Plaintiff."**


        #     **Note:** Make sure to triple-check data before proceeding to the next step.

        #     **Generate JSON object with key-value pairs:**
        #     - **Note:** Always generate the JSON object with these keys.
        #     - **Creditor:** Plaintiff(s) data (only the name). Exclude "Attorney for Plaintiff" information.
        #     - **Balance:** Plaintiff’s Balance Owed data (if available),
        #     - **Companies Sued:** Ensure to include all defendants in this CSV list, regardless of other available data.
        #     - **First Name:** Extracted First Name of Defendant,
        #     - **Last Name:** Extracted Last Name of Defendant,
        #     - **Phone Number:** Defendant’s Phone Numbers,
        #     - **Email:** Defendant’s Email Addresses,
        #     - **Address:** Defendant’s Address,
        #     - **County:** Court County data,
        #     - **Case Number:** Case Number data,
        #     - **Notes:** Always include a brief summary about the case.
        # """,

        instructions="""

            **Primary Objective:**
            - **Always return a JSON object in the response containing the extracted data with all the key value pairs. **
            
            **File Utilization:**
            - **Use all available files to extract the required data as accurately and completely as possible. If there is more than one exhibit provided, analyze the first exhibit to see it it contains all the data. If it doesn't only then move on to analyzing the next file.**
            
            **Triple-Check Protocol:**
            - **Ensure thorough verification at three stages:**
            1. **Initial Extraction:** Verify the completeness of data during the first extraction from files.
            2. **Post-Processing Review:** Recheck the data after any processing or conversion.
            3. **Pre-Submission Confirmation:** Confirm the accuracy and completeness of all data before finalizing the JSON object.
            
            **Extract data from Summons:**
            - **Plaintiff(s) and Defendant(s) Names:**
            - **Plaintiff(s):** Extract Plaintiff listed from Summons (data type: string or "unavailable" if not present). This is always located on page one of the Summons file. Disregard any data that belongs to Attorney for Plaintiff, this includes the attorney's name, phone number, or email.
            --- **Note:** In Kings County, the Plaintiff(s) are always located on page 1 of the Summons file.
            - **Plaintiff(s) Data:**
            -- **Balance Owed:** (data type: float).
            -- **Balance Possible Keywords:** "the sum of $", "in the amount of", "damages", 'damages owed", "balance of", "no event less than", "monetary compensation", "financial damages",  etc.
            --- **Note:** You must return the balance owed. The Balance Owed is the amount the plaintiff is sueing the defendant(s) for it is always found in the Summons. Use the keywords list and other similar terms as context identifiers to locate the amount due. After you have found it, double check the Summons to make sure you have the correct value.
            - **Defendant(s):** Extract Defendants listed from Summons (data type: string or "unavailable" if not present).
            - **Primary Defendant:** Extract the first name from listed Defendants that is not a business name, that is the primary defendant (data type: string or "unavailable" if not present).
            - **Address:** Extract any addresses present from listed with Defendants (data type: string, CSV list or "unavailable" if not present).

            - **Note:** If there is only one Defendant listed, that is the primary Defendant.

            **Extract data from Exhibit files (if available):**
            2. **Defendant(s) Data:**
            - **Note:** Extract the following data for Defendant(s) as the primary source of data if available. If not available, attempt to extract the data from the Summons.
            - **First Personal Name (non-business):** (data type: string or "unavailable" if not present).
            - **Phone Numbers:** (data type: string, CSV list or "unavailable" if not present).
            - **Email Addresses:** (data type: string, CSV list or "unavailable" if not present).
            - **Note:** The address can almost always be found in the Summons.
            - **Companies Sued:** (data type: string, CSV list). Include all defendants in this list, even if it's the only data available about them.
            3. **Court County Data:** (data type: string or "unavailable" if not present).
            4. **Case Number:** (data type: string or "unavailable" if not present). This is the court ID for example "######/YEAR aka 536793/2023" or "E#######".

            **Data Processing Instructions:**
            - **Convert Balance value to a float number with two decimal places.**
            - **Disregard any data labeled "Attorney for Plaintiff."**


            **Note:** At this point go back and check your work. Make sure to triple-check data before proceeding to the next step.

            **Generate JSON object with key-value pairs:**
            - **Note:** Always generate the JSON object with these keys.
            - **Creditor:** Plaintiff(s) data (only the name). Exclude "Attorney for Plaintiff" information.
            - **Balance:** Plaintiff’s Balance Owed data (if available),
            - **Companies Sued:** Ensure to include all defendants in this CSV list, regardless of other available data.
            - **First Name:** Extracted First Name of Defendant,
            - **Last Name:** Extracted Last Name of Defendant,
            - **Phone Number:** Defendant’s Phone Numbers,
            - **Email:** Defendant’s Email Addresses,
            - **Address:** Defendant’s Address,
            - **County:** Court County data,
            - **Case Number:** Case Number data,
            - **Notes:** Always include a brief summary about the case.

        """,
        name="MyAssistant",
        tools=[{"type": "retrieval"}],
        # model="gpt-4-1106-preview",
        model="gpt-3.5-turbo-1106",
        file_ids=file_ids
    )

    assistant_id = my_assistant.id

    print(f"Assistant ID: {assistant_id}")

    return assistant_id


def create_message(client, thread_id, file_ids):
    # /v1/threads/thread_0spnmrJpArrNGRUmzt2IisHo/messages

    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content="Please analyze the provided files and directly return the resulting JSON object. Refrain from giving any explanations, summaries, or additional comments.",
        file_ids=file_ids
    )
    print(f"Created Message ID: {message.id}")


def run_thread(client, thread_id, assistant_id):

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )

    return run.id


def create_thread(client):

    client = OpenAI(
        api_key=os.getenv('OPENAI_API'),
    )

    thread = client.beta.threads.create()

    print(f"Thread ID: {thread.id}")

    return thread.id


def extract_json(multi_line_string):
    try:
        # Splitting the string into lines
        lines = multi_line_string.split('\n')

        # Finding the lines that contain the JSON object
        json_str = ''
        json_started = False
        for line in lines:
            # Check for the start of the JSON object
            if '{' in line:
                json_started = True

            # If the JSON object has started, append the line
            if json_started:
                json_str += line

            # Check for the end of the JSON object
            if '}' in line:
                break

        # Convert the JSON string to a JSON object
        return json.loads(json_str)
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_message(client, thread_id, message_id):

    thread_message = client.beta.threads.messages.retrieve(
        thread_id=thread_id, message_id=message_id)
    thread_message_contents = list(thread_message.content)
    thread_message_dict = dict(thread_message_contents[0])
    thread_message_list = list(thread_message_dict['text'])[1]
    thread_message_value = thread_message_list[1]

    return thread_message_value


def get_messages(client, thread_id):

    thread_messages = list(
        client.beta.threads.messages.list(thread_id=thread_id))
    message_ids = []
    for thread_message in thread_messages:
        message_ids.append(thread_message.id)
        print(f'Retrieving Messasge ID: {thread_message.id}')
    return message_ids


def get_status(client, thread_id, run_id):

    run = client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run_id
    )

    return run.status


def get_steps(client, thread_id, run_id):
    run_steps = client.beta.threads.runs.steps.list(
        thread_id=thread_id,
        run_id=run_id
    )
    print(run_steps)
    return run_steps


def list_of_file_paths(pdf_directory):
    # Dynamically get the PDF directory path in the ./tmp/pdf directory
    pdf_dir = os.path.join(os.getcwd(), "tmp", "pdf")

    # Get a list of all files in the PDF directory
    files = os.listdir(pdf_directory)

    # Create a dictionary to group files by their PDF file name
    pdf_files_dict = {}

    # Group files by their PDF file name
    for file_name in files:
        pdf_name = file_name.split('_')[0]
        # Get the full file path
        file_path = os.path.join(pdf_directory, file_name)
        if pdf_name in pdf_files_dict:
            pdf_files_dict[pdf_name].append(file_path)
        else:
            pdf_files_dict[pdf_name] = [file_path]

    # Create a list to store groups of files with the same PDF file name
    same_pdf_files = [
        files for files in pdf_files_dict.values() if len(files) >= 1]

    # Return the list of groups of files with the same PDF file name
    return same_pdf_files


def upload_file(client, file_path):

    file_upload_response = client.files.create(
        file=open(file_path, "rb"),
        purpose="assistants"
    )
    print(
        f"File Name: {file_upload_response.filename} & File ID: {file_upload_response.id}")

    return file_upload_response.id


def process_files(directory):
    for file_name in os.listdir(directory):
        # Check if the file is a PDF
        if file_name.endswith(".pdf"):
            file_path = os.path.join(directory, file_name)
            print(f'File to be uploaded: {file_name}')
            print(f'File path: {file_path}')


def save_to_csv(data, filename):
    """
    Save a list of dictionaries to a CSV file.

    Parameters:
    data (list of dict): The data to be written to the CSV.
    filename (str): The name of the output CSV file.
    """
    if not data:
        print("The data list is empty. No file was created.")
        return

    # Determine the fieldnames (keys of the dictionary)
    try:
        fieldnames = data[0].keys()

        # Writing to the csv file
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write the header
            writer.writeheader()

            # Write the data rows
            for row in data:
                if row != None:
                    writer.writerow(row)

        print(f"Data successfully written to {filename}")
    except Exception as e:
        print(f"Error: {e} {data}")
        pass


def send_to_chatgpt(csv_directory, pdf_directory):

    load_dotenv()

    client = OpenAI(
        api_key=os.getenv('OPENAI_API'),
    )

    # Get a list of all files in the PDF directory
    case_files = list_of_file_paths(pdf_directory)
    responses = []

    for case_file in case_files:
        analysis_start_time = datetime.now()
        print(f'Analysis Start Time: {analysis_start_time}')
        file_ids = []
        for file in case_file:
            file_id = upload_file(client, file)
            file_ids.append(file_id)

        assistant_id = create_assistant(client, file_ids)
        thread_id = create_thread(client)
        create_message(client, thread_id, file_ids)
        time.sleep(1)
        run_id = run_thread(client, thread_id, assistant_id)
        print('Starting ChatGPT Analysis...')
        time.sleep(2)
        while True:
            status = get_status(client, thread_id, run_id)

            if status == 'failed':
                assistant_id = create_assistant(client, file_ids)
                thread_id = create_thread(client)
                create_message(client, thread_id, file_ids)
                time.sleep(1)
                run_id = run_thread(client, thread_id, assistant_id)
                time.sleep(2)
            elif status == 'in_progress':
                print(f'Chat Status: {status}')
                time.sleep(20)
                continue
            elif status == 'completed':
                break
            else:
                time.sleep(5)

        message_ids = get_messages(client, thread_id)
        message = get_message(client, thread_id, message_ids[0])
        print(f'''
              ChatGPT Response:
                {message}
              '''
              )
        message_dict = extract_json(message)
        # print(f'''
        #       JSON Object:
        #         {message_dict}
        #       '''
        #       )
        responses.append(message_dict)
        analysis_end_time = datetime.now()
        print(f'Analysis End Time: {analysis_end_time}')
        analysis_time = analysis_end_time - analysis_start_time
        print(f'Analysis Time: {analysis_time}')
        print('---------------------------------')
    file_path = os.path.join(csv_directory, "chatgpt-results.csv")
    save_to_csv(responses, file_path)
