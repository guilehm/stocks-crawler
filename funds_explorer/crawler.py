import logging
import os
import sys

import requests
from requests import RequestException
from requests.models import PreparedRequest
from scrapy.selector import Selector

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

FUNDS_EXPLORER_URL = os.getenv('FUNDS_EXPLORER_URL')
ENDPOINT_FUNDS_LIST = '/funds'


class FundsCrawler:
    def __init__(self, base_url=FUNDS_EXPLORER_URL, db=None):
        self.base_url = base_url
        self.response = None
        self.db = db

    def _prepare_url(self, endpoint, **params):
        url = f'{self.base_url}/{endpoint}'
        prepared_request = PreparedRequest()
        prepared_request.prepare_url(url, params)
        return prepared_request.url

    def get_response(self, endpoint, **params):
        url = self._prepare_url(endpoint, **params)
        response = requests.get(url)
        try:
            response.raise_for_status()
        except RequestException:
            logging.error('Could not request', exc_info=True)
        else:
            self.response = Selector(text=response.text)
        return self.response

    def parse_funds_list(self, endpoint=ENDPOINT_FUNDS_LIST, **params):
        def extract_fund_data(item):
            return dict(
                name=item.xpath('.//span[@class="name"]/text()').get(),
                symbol=item.xpath('.//span[@class="symbol"]/text()').get(),
                admin=item.xpath('.//span[@class="admin"]/text()').get('').strip(),
            )

        response = self.get_response(endpoint, **params)
        funds_list = response.xpath(
            '//div[@id="fiis-list-container"]/div/div[contains(@id, "item-")]'
        )
        funds_data = [extract_fund_data(fund) for fund in funds_list]
        return funds_data
