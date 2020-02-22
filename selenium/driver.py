
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

CHROME_DRIVER_LOCATION = os.getenv('CHROME_DRIVER_LOCATION')


class Driver:

    def __init__(self, location=CHROME_DRIVER_LOCATION, headless=True, user_agent=''):
        self.location = location
        self.headless = headless
        self.user_agent = user_agent

    def _get_options(self):
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        if self.user_agent:
            chrome_options.add_argument(f'user-agent={self.user_agent}')
        if self.headless:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
        return chrome_options

    def get_driver(self):
        params = dict(options=self._get_options())
        if self.location:
            params.update(drive_location=self.location)
        return webdriver.Chrome(**params)
