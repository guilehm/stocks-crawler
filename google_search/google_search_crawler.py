import logging
import os
import sys
from datetime import datetime, timedelta
from decimal import Decimal, DecimalException

from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from driver_builder.builder import Driver
from utils.helpers import convert_decimal_for_db

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

BASE_URL = 'https://www.google.com/search?' \
           'q={symbol}&oq={symbol}&aqs=chrome.0.69i59j69i60l3j0l2.1532j1j7&sourceid=chrome&ie=UTF-8'

THOUSAND_SEPARATOR = os.getenv('THOUSAND_SEPARATOR', '.')


class GoogleSearchCrawler:

    def __init__(self, symbol='bidi4', db=None, headless=True):
        self.db = db
        self.symbol = symbol
        self.driver = Driver(headless=headless).get_driver()
        self.url = BASE_URL.format(symbol=symbol)

    def save_data(self, data, collection='googleSearch'):
        if not self.db:
            logging.error('Could not save data. Please choose a database')
            return
        collection = self.db[collection]
        return collection.insert_one(convert_decimal_for_db(data))

    def _get_page(self):
        self.driver.get(self.url)

    @staticmethod
    def convert_to_decimal(value):
        text_value = value.text
        if THOUSAND_SEPARATOR == ',':
            text_value = text_value.replace(',', '')
        else:
            text_value = text_value.replace('.', '').replace(',', '.')
        try:
            value_decimal = Decimal(text_value)
        except DecimalException:
            value_decimal = None
            logging.exception(
                f'Could not convert value {value.text} to Decimal from {text_value}',
                exc_info=True,
            )
        return value_decimal

    def _validate_stock_data(self, name, symbol, value, time):
        value_decimal = self.convert_to_decimal(value)
        return dict(
            name=name.text,
            symbol=self.symbol.upper(),
            symbolDetail=symbol.text,
            value=value_decimal,
            time=time.text,
            crawlDate=datetime.utcnow() - timedelta(hours=3),
        )

    def wait_for_element(self, condition, value, timeout=5):
        logging.info(f'Waiting for {value}')
        return WebDriverWait(
            driver=self.driver,
            timeout=timeout,
        ).until(expected_conditions.presence_of_element_located(
            (condition, value,)
        ))

    def get_stock_data(self, save=True):
        logging.info(f'Trying to get actual price for {self.symbol}')
        self._get_page()
        try:
            name = self.wait_for_element(By.XPATH, '//div[@class="oPhL2e"]')
            symbol = self.driver.find_element_by_xpath('//div[@class="HfMth"]')
            value = self.driver.find_element_by_xpath('//span[@jsname="vWLAgc"]')
            time = self.driver.find_element_by_xpath('//span[@jsname="ihIZgd"]')
        except NoSuchElementException as e:
            logging.exception(f'Unable to locate element "vWLAgc": {e}')
            raise
        except TimeoutException:
            logging.exception('The element "vWLAgc" was not rendered.')
            raise
        except Exception as e:
            logging.exception(f'Could not get element: {e}')
            raise
        else:
            data = self._validate_stock_data(name, symbol, value, time)
            if save:
                self.save_data(data)
            return data
        finally:
            self.driver.quit()
