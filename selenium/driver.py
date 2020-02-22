import os

from selenium import webdriver

CHROME_DRIVER_LOCATION = os.getenv('CHROME_DRIVER_LOCATION')


class Driver:

    def get_driver(self, location=CHROME_DRIVER_LOCATION):
        if location:
            return webdriver.Chrome(location)
        return webdriver.Chrome()

