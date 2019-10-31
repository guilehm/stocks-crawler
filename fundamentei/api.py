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
        'query=&hitsPerPage=100&page=NUM_PAGE&facetFilters=%5B%5B%22type%3ABRAZILIAN_COMPANY%22%5D%5D"}]}'


class Fundamentei:
    def __init__(self, base_url=BASE_URL, params=params, query=query):
        self.base_url = base_url
        self.params = params
        self.query = query
        self.results = []

    def get_data(self, force_update=False, page=0):
        response = requests.post(
            self.base_url,
            params=self.params,
            data=self.query.replace('NUM_PAGE', str(page))
        )
        try:
            response.raise_for_status()
        except RequestException:
            logging.error(response.text)
            return

        return response.json()

    def get_results(self, page=0):
        data = self.get_data(page=page)
        return data['results'][0]['hits']

    def get_all_results(self):
        self.results = []
        for page in range(100):
            results = self.get_results(page=page)
            if not results:
                break
            self.results += results
        return self.results
