import requests
from pymongo import MongoClient
from scrapy.selector import Selector

BASE_URL = 'https://eduardocavalcanti.com'
MONGO_URL = 'mongodb://localhost:27017/'
DB_NAME = 'stocks'


class BaseSpider:
    def __init__(self, login, password, base_url=BASE_URL, mongo_url=MONGO_URL, db_name=DB_NAME):
        self.mongo_client = MongoClient(mongo_url)
        self.db = self.mongo_client[db_name]
        self.base_url = base_url
        self.authenticated = False
        self.login = login
        self.password = password
        self.session = None
        self.response = None
        self.url = None

    def _create_data_login(self):
        return {
            'action': 'arm_shortcode_form_ajax_action',
            'form_random_key': '102_06blAsIBsu',
            'user_login': f'{self.login}',
            'user_pass': f'{self.password}',
            'rememberme': '',
            'arm_action': 'please-login',
            'redirect_to': f'{self.base_url}',
            'isAdmin': '0',
            'referral_url': f'{self.base_url}/login/',
            'form_filter_kp': '9',
            'form_filter_st': '1566007996',
            'arm_nonce_check': '80161f9f45'
        }

    def _authenticate(self):
        session = requests.session()
        session.post(
            f'{self.base_url}/wp-admin/admin-ajax.php',
            data=self._create_data_login(),
        )
        response = session.get(f'{self.base_url}/dashboard/')
        if 'AFLT' in response.text:
            self.authenticated = True
            self.session = session
        else:
            raise Exception('Could not authenticate')

    def get_response(self, url, force_update=False):
        if not self.authenticated:
            self._authenticate()
        if self.response and self.url == url and not force_update:
            return self.response
        self.url = url
        response = self.session.get(url)
        self.response = Selector(text=response.text)
        return self.response

    def save_data(self, data, collection):
        collection = self.db[collection]
        many = not isinstance(data, dict) and len(data) > 1
        if many:
            return collection.insert_many(data)
        return collection.insert_one(data)


class StockSpider(BaseSpider):
    def parse_stocks(self, url, save=False):
        response = self.get_response(url)
        stocks = [extract_from_links(link, 'code') for link in response.xpath(
            '//h2[@class="entry-title"]/a'
        )]
        names = [name.strip() for name in response.xpath(
            '//article//div[@class="entry-content entry-summary"]//text()'
        ).getall() if name and name.strip()]
        [stock.update(name=name) for stock, name in list(zip(stocks, names))]
        if save:
            self.save_data(stocks, 'stocks')
        return stocks

    def _get_response_fundamentalist_analysis(self, stock, url=None):
        if not url:
            url = f'{self.base_url}/an_fundamentalista/{stock}/'
        return self.get_response(url)

    def parse_fundamentalist_analysis_rate(self, stock, url=None):
        response = self._get_response_fundamentalist_analysis(stock, url)
        data = [text.strip() for text in response.xpath(
            '//span[contains(@class, "rating-result  mrp-shortcode")]/span/text()'
        ).getall()]
        data = [convert_to_float(text.replace('/10', '').strip('(').strip(')')) for text in data]
        return dict(
            rate=data[0],
            votes=data[1],
        )

    def parse_fundamentalist_analysis_video(self, stock, url=None):
        response = self._get_response_fundamentalist_analysis(stock, url)
        return dict(
            video=response.xpath(
                './/section[@class="analise-video"]//iframe/@src'
            ).get('').strip('//')
        )

    def parse_fundamentalist_analysis_chart(self, stock, url=None):
        response = self._get_response_fundamentalist_analysis(stock, url)
        return dict(
            chart=response.xpath(
                '//section/iframe[contains(@src, "s.tradingview.com/bovespa/")]/@src'
            ).get()
        )

    def parse_fundamentalist_analysis_company_data(self, stock, save=False, url=None):
        response = self._get_response_fundamentalist_analysis(stock, url)
        company, governance = response.xpath(
            './/table[@class="table table-responsive table-condensed infoDados"]'
        )
        data = dict(
            company=extract_from_company_data(company),
            governance=extract_from_company_data(governance)
        )
        if save:
            self.save_data(data, 'fundamentalistAnalysis')
        return data

    def parse_fundamentalist_analysis_table(self, stock, save=False, url=None):
        response = self._get_response_fundamentalist_analysis(stock, url)
        table = response.xpath(
            '//table[@class="table table-hover table-condensed table-responsive analise"]'
        )
        headers = [text.strip() for text in table.xpath(
            './thead/tr//text()'
        ).getall() if text.strip()]
        trs = table.xpath('./tbody/tr')
        rows = [extract_from_tr(tr) for tr in trs if tr]
        data = [merge_keys_and_values(headers, row) for row in rows if row]
        if save:
            self.save_data(data, 'fundamentalistAnalysis')
        return dict(fundamentalistAnalysis=data)

    def extract_all_fundamentalist_data(self, stock, save=False, url=None):
        output = dict()
        output.update(self.parse_fundamentalist_analysis_company_data(stock, url=url))
        output.update(self.parse_fundamentalist_analysis_rate(stock, url=url))
        output.update(self.parse_fundamentalist_analysis_video(stock, url=url))
        output.update(self.parse_fundamentalist_analysis_chart(stock, url=url))
        output.update(self.parse_fundamentalist_analysis_table(stock, url=url))
        if save:
            print(f'saving for {stock}')
            self.save_data(output, 'fundamentalistAnalysis')
        return output

    def extract_data_for_all_stocks(self, save=True):
        stocks_collection = self.db.stocks
        stocks = [stock for stock in stocks_collection.find()]
        for stock in stocks:
            self.extract_all_fundamentalist_data(stock=stock['code'], save=save, url=stock['url'])


def convert_to_float(value):
    try:
        converted = float(value)
    except ValueError:
        converted = value.replace(',', '.')
        return convert_to_float(converted)
    return converted


def extract_from_company_data(row):
    data = [text.strip().strip(':') for text in row.xpath('.//text()').getall() if text.strip()]
    output = dict()
    key, value = None, None
    for number, i in enumerate(data):
        if number % 2 == 0:
            key = i
        else:
            value = i
        if value:
            output.update({key: value})
            value = None
    return output


def extract_from_links(node, name='name'):
    return {
        name: node.xpath('text()').get().strip(),
        'url': node.attrib['href']
    }


def extract_from_tr(tr):
    data = [a.strip() for a in tr.xpath('.//text()').getall() if a.strip()]
    return data or None


def merge_keys_and_values(keys, values):
    if values:
        tuples = list(zip(keys, values))
        return {key.replace('.', ''): value for key, value in tuples}
