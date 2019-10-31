import logging
import sys

import requests
from requests import RequestException

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

BASE_URL = 'https://19ba7tbxn5-dsn.algolia.net/1/indexes/*/queries'

params = {
    'x-algolia-agent': 'Algolia%20for%20JavaScript%20(3.34.0)%3B%20Browser',
    'x-algolia-application-id': '19BA7TBXN5',
    'x-algolia-api-key': '931073b87323ba15c33974ba4e154e05'
}

query = '{"requests":[{"indexName":"assets","params":"' \
        'query=&hitsPerPage=100&page=0&facetFilters=%5B%5B%22type%3ABRAZILIAN_COMPANY%22%5D%5D"}]}'


class Fundamentei:
    def __init__(self, base_url=BASE_URL, params=params, query=query):
        self.base_url = base_url
        self.params = params
        self.query = query
        self.data = None

    def get_data(self, force_update=False):
        if self.data and not force_update:
            return self.data

        response = requests.post(self.base_url, params=self.params, data=self.query)
        try:
            response.raise_for_status()
        except RequestException:
            logging.error(response.text)
            return

        self.data = response.json()
        return self.data

    def get_results(self):
        data = self.get_data()
        return data['results'][0]['hits']