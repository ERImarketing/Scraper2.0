# Standard library imports
import time


# Local application/library-specific imports
from scraper import scraper

# Main program execution
if __name__ == "__main__":

    # Run the scraper
    scraper()

    # Sleep for 50 seconds at the end
    time.sleep(10800)
