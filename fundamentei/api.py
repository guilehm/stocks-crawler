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
    def __init__(self, base_url=BASE_URL, params=params, query=query, db=None):
        self.base_url = base_url
        self.params = params
        self.query = query
        self.db = db
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

    def get_all_results(self, update_db=False, drop_old_collection=True):
        self.results = []
        for page in range(100):
            results = self.get_results(page=page)
            if not results:
                break
            self.results += results
        if update_db:
            self.save_data(self.results, 'hits', drop_old_collection=drop_old_collection)
        return self.results

    def save_data(self, data, collection, drop_old_collection=False):
        if not self.db:
            logging.error('Could not save data. Please choose a database')
            return
        collection = self.db[collection]
        many = not isinstance(data, dict) and len(data) > 1

        if drop_old_collection:
            collection.drop()

        if many:
            return collection.insert_many(data)
        return collection.insert_one(data)
