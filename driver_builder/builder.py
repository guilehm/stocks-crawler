import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/60.0.3112.50 Safari/537.36'
DRIVER_NAME = os.getenv('DRIVER_NAME', 'chromedriver73')
CHROMEDRIVER_PATH = os.getenv('CHROMEDRIVER_PATH')
GOOGLE_CHROME_BIN = os.getenv('GOOGLE_CHROME_BIN')


class Driver:

    @staticmethod
    def __get_location():
        return CHROMEDRIVER_PATH or f'{os.getcwd()}/driver_builder/chromedriver/{DRIVER_NAME}'

    def __init__(self, headless=True, user_agent=USER_AGENT):
        self.location = self.__get_location()
        self.headless = headless
        self.user_agent = user_agent

    def _get_options(self):
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        if self.user_agent:
            chrome_options.add_argument(f'user-agent={self.user_agent}')
        if GOOGLE_CHROME_BIN:
            chrome_options.binary_location = GOOGLE_CHROME_BIN
        if self.headless:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
        return chrome_options

    def get_driver(self):
        return webdriver.Chrome(self.location, options=self._get_options())
