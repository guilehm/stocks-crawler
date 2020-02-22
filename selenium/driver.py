import os

from selenium.webdriver.chrome.options import Options

from selenium import webdriver

DRIVER_NAME = os.getenv('DRIVER_NAME', 'chromedriver73')


class Driver:

    def __init__(self, driver_name=DRIVER_NAME, headless=True, user_agent=''):
        self.location = f'{os.getcwd()}/selenium/chromedriver/{driver_name}'
        self.headless = headless
        self.user_agent = user_agent

    def _get_options(self):
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        if self.user_agent:
            chrome_options.add_argument(f'user-agent={self.user_agent}')
        if self.headless:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
        return chrome_options

    def get_driver(self):
        return webdriver.Chrome(self.location, options=self._get_options())
