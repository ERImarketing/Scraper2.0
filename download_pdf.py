import time
from selenium.webdriver.common.by import By

from init_driver import init_driver


def download_search_result(driver, url):

    base_url = "https://iapps.courts.state.ny.us/nyscef/"

    driver.get(url)

    time.sleep(5)

    # Specify the keywords you're looking for (case-insensitive)
    keywords = ['SUMMONS', 'EXHIBIT']  # Replace with your keywords

    # Construct XPath expression to find links containing any of the keywords
    xpath_expression = " | ".join(
        [f"//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{keyword.lower()}')]" for keyword in keywords])

    # Find elements using the constructed XPath
    links = driver.find_elements(By.XPATH, xpath_expression)

    # Extract and print the URLs
    for link in links:
        link = link.get_attribute('href')
        print(link)
        driver.get(link)
        time.sleep(5)
        # Execute print command to save page as PDF
        print_settings = {
            'recentDestinations': [{
                'id': 'Save as PDF',
                'origin': 'local',
                'account': '',
            }],
            'selectedDestinationId': 'Save as PDF',
            'version': 2,
            'isHeaderFooterEnabled': False  # Disable header and footer
        }
        driver.execute_cdp_cmd('Page.printToPDF', print_settings)
        print(f'Downloaded pdf for {link}.')
