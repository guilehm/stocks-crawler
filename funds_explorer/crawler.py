import logging
import os
import sys

import requests
from requests import RequestException
from requests.models import PreparedRequest
from scrapy.selector import Selector

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

FUNDS_EXPLORER_URL = os.getenv('FUNDS_EXPLORER_URL')
ENDPOINT_FUNDS_LIST = 'funds'
ENDPOINT_FUNDS_DETAIL = 'funds/{symbol}'
ENDPOINT_RANKING_TABLE = 'ranking'


class FundsCrawler:
    def __init__(self, base_url=FUNDS_EXPLORER_URL, db=None):
        self.base_url = base_url
        self.response = None
        self.url = None
        self.db = db

    def _prepare_url(self, endpoint, **params):
        url = f'{self.base_url}/{endpoint}'
        prepared_request = PreparedRequest()
        prepared_request.prepare_url(url, params)
        return prepared_request.url

    def get_response(self, endpoint, force_update=False, **params):
        url = self._prepare_url(endpoint, **params)
        if self.response and not force_update and self.url == url:
            return self.response
        response = requests.get(url)
        try:
            response.raise_for_status()
        except RequestException:
            self.response = None
            logging.error('Could not request', exc_info=True)
        else:
            self.url = url
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
        return list(map(extract_fund_data, funds_list))

    def parse_funds_detail(self, symbol, endpoint=ENDPOINT_FUNDS_DETAIL, **params):
        complete_endpoint = endpoint.format(symbol=symbol)
        response = self.get_response(endpoint=complete_endpoint, **params)
        main_indicators = response.xpath(
            './/div[@id="main-indicators-carousel"]//div[@class="carousel-cell"]'
        )

        def get_main_indicators_data(res):
            title = res.xpath('./span[@class="indicator-title"]/text()').get('').strip()
            value = res.xpath('./span[@class="indicator-value"]/text()').get('').strip()
            return {title: value}

        return list(map(get_main_indicators_data, main_indicators))
