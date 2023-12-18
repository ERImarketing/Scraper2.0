# Import necessary libraries
from datetime import date
from random_delay import random_delay
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from exit_scraper import exit_scraper


def select_court(driver, anticaptcha_key, court_index):
    """
    Selects a court on a web page, enters today's date, and submits a form.

    :param driver: The Selenium WebDriver object.
    :param anticaptcha_key: Your AntiCaptcha API key.
    :param court_index: Index of the court to be selected.
    :return: The updated court index.
    """

    # Get today's date
    today = date.today()

    # Open the website
    url = "https://iapps.courts.state.ny.us/nyscef/CaseSearch?TAB=courtDateRange"
    driver.get(url)

    # Introduce a random delay to mimic human behavior
    random_delay(5, 7)

    # Locate and interact with the court selection dropdown
    court_dropdown = driver.find_element(By.ID, 'selCountyCourt')
    court_options = court_dropdown.find_elements(By.TAG_NAME, 'option')
    try:
        # pick_court = court_options[court_index]
        pick_court = court_options[23]  # TESTING PURPOSES ONLY
    except:
        exit_scraper(driver)
    current_court = pick_court.text
    pick_court.click()

    # Introduce another random delay
    random_delay(5, 7)

    # Fill in the date input field with today's date
    filing_date_input = driver.find_element(By.ID, 'txtFilingDate')
    filing_date_input.clear()
    random_delay(5, 7)
    filing_date_input.send_keys(today.strftime("%m/%d/%Y"))
    # filing_date_input.send_keys(today.strftime("11/20/2023")) # TESTING PURPOSES ONLY

    # Print information about the selected court and index
    print(f'Currently Searching: {current_court}...')
    print(f'At Index Number: {court_index}...')
    random_delay(3, 5)

    # Submit the form by sending an Enter key press to the date input field
    filing_date_input.send_keys(Keys.ENTER)

    # Increment the court index for the next iteration
    return court_index + 1


# Select court loop with try/except block
def select_court_try_except(driver, anticaptcha_key, court_index):
    try:
        return select_court(driver, anticaptcha_key, court_index)
    except:
        return select_court(driver, anticaptcha_key, court_index)
