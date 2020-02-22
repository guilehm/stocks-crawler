import logging
import sys

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

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

    def get_stock_value(self):
        logging.info(f'Trying to get actual price for {self.symbol}')
        self._get_page()
        try:
            name = self.wait_for_element(By.XPATH, '//div[@class="oPhL2e"]')
            symbol = self.wait_for_element(By.XPATH, '//div[@class="HfMth"]')
            value = self.wait_for_element(By.XPATH, '//span[@jsname="vWLAgc"]')
            return dict(
                name=name.text,
                symbol=symbol.text,
                value=value.text,
            )
        except TimeoutException:
            logging.exception('Could not find element "vWLAgc"', exc_info=True)
        except Exception as e:
            logging.exception(f'Could not get element: {e}')
        finally:
            self.driver.quit()
