from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os

ROOT_PATH = Path(__file__).parent.parent
CHROMEDRIVER_NAME = 'chromedriver.exe'
CHROMEDRIVER_PATH = ROOT_PATH / 'bin' / CHROMEDRIVER_NAME


def launchBrowser(*options):
    while True:
        chrome_options = webdriver.ChromeOptions()

        if options is not None:
            for option in options:
                chrome_options.add_argument(option)

        if os.environ.get('SELENIUM_HEADLESS') == '1':
            chrome_options.add_argument('--headless')

        chrome_service = Service(executable_path=str(CHROMEDRIVER_PATH))
        browser = webdriver.Chrome(
            service=chrome_service, options=chrome_options)
        return browser


if __name__ == '__main__':
    browser = launchBrowser()
    browser.get('http://127.0.0.1:8000/')
    while True:
        pass
