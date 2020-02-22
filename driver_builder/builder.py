import os

from driver_builder.webdriver.chrome.options import Options

from driver_builder import webdriver

DRIVER_NAME = os.getenv('DRIVER_NAME', 'chromedriver73')
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/60.0.3112.50 Safari/537.36'


class Driver:

    def __init__(self, driver_name=DRIVER_NAME, headless=True, user_agent=USER_AGENT):
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
