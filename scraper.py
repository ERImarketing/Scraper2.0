# Standard library imports
import os
import time

# Related third-party imports
import pandas as pd
from dotenv import load_dotenv

# Local application/library-specific imports
from extract_court_results import extract_table_data
from init_driver import init_driver
from pagination import find_and_click_next_page
from random_delay import random_delay
from select_court import select_court_try_except as select_court
from sort_results import sort_results
from download_individual_search_results import download_search_result
from send_to_gpt import process_files
from chatgpt_cleanup import cleanup

# Define a function to initialize the Chrome driver


# Scraper


def scraper():

    # Load environment variables from a .env file
    load_dotenv()
    webhook_url = os.getenv('WEBHOOK_URL')
    anticaptcha_key = os.getenv('ANTICAPTCHA_API_KEY')

    # Initialize the Chrome driver
    driver = init_driver()

    # Set court index to 1 to start with the first court
    court_index = 1

    # Select a court using a custom function and anticaptcha_key
    court_index = select_court(driver, anticaptcha_key, court_index)
    random_delay(3, 5)

    # Check if the results page is displayed and sort results
    sort_results(driver, anticaptcha_key)

    random_delay(5, 7)

    # Create a DataFrame to store the results
    existing_df = pd.DataFrame(columns=['Link', 'Case #/Received Date',
                                        'eFiling Status/Case Status', 'Caption', 'Court/Case Type', 'Empty'])
    html = driver.page_source
    existing_df = extract_table_data(html, existing_df)

    # Loop through courts until a certain condition is met (court_index < 63)
    while court_index <= 61:
        # Select a court, introduce a random delay, and sort results
        court_index = select_court(driver, anticaptcha_key, court_index)
        random_delay(5, 7)
        sort_results(driver, anticaptcha_key)
        random_delay(5, 7)
        html = driver.page_source
        existing_df = extract_table_data(html, existing_df)

        # Find and click the "Next Page" button and update the DataFrame
        existing_df = find_and_click_next_page(
            driver, anticaptcha_key, existing_df, court_index)

        # Dropping duplicates based on the 'Link' column, keeping the first occurrence
        df_unique = existing_df.drop_duplicates(
            subset='Link', keep='first')

        print(df_unique)
        # Save the DataFrame to a CSV file every 5 courts
        if court_index == 61:

            for _, row in df_unique.iterrows():
                data = row.to_dict()

                download_search_result(driver, data['Link'])

            process_files('./tmp/pdf')

    cleanup()
    print('Scraper Finished')
