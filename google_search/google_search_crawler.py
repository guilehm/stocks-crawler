import logging
import sys

from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from decimal import Decimal, DecimalException

from datetime import datetime, timedelta

from driver_builder.builder import Driver

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

BASE_URL = 'https://www.google.com/search?' \
           'q={symbol}&oq={symbol}&aqs=chrome.0.69i59j69i60l3j0l2.1532j1j7&sourceid=chrome&ie=UTF-8'


class GoogleSearchCrawler:

    def __init__(self, symbol='bidi4'):
        self.driver = Driver().get_driver()
        self.symbol = symbol
        self.url = BASE_URL.format(symbol=symbol)

    def _get_page(self):
        self.driver.get(self.url)

    def wait_for_element(self, condition, value, timeout=5):
        logging.info(f'Waiting for {value}')
        return WebDriverWait(
            driver=self.driver,
            timeout=timeout,
        ).until(expected_conditions.presence_of_element_located(
            (condition, value,)
        ))

    def _validate_stock_data(self, name, symbol, value, time):
        try:
            value_decimal = Decimal(value.text)
        except DecimalException:
            value_decimal = None
            logging.exception(
                f'Could not convert value {value} to Decimal',
                exc_info=True,
            )
        return dict(
            name=name.text,
            symbol=symbol.text,
            value=value_decimal,
            time=time.text,
            crawlDate=datetime.utcnow() - timedelta(hours=3),
        )

    def get_stock_data(self):
        logging.info(f'Trying to get actual price for {self.symbol}')
        self._get_page()
        try:
            name = self.wait_for_element(By.XPATH, '//div[@class="oPhL2e"]')
            symbol = self.driver.find_element_by_xpath('//div[@class="HfMth"]')
            value = self.driver.find_element_by_xpath('//span[@jsname="vWLAgc"]')
            time = self.driver.find_element_by_xpath('//span[@jsname="ihIZgd"]')
        except NoSuchElementException as e:
            logging.exception(f'Unable to locate element "vWLAgc": {e}')
        except TimeoutException:
            logging.exception('The element "vWLAgc" was not rendered.')
        except Exception as e:
            logging.exception(f'Could not get element: {e}')
        else:
            return self._validate_stock_data(name, symbol, value, time)
        finally:
            self.driver.quit()
