import requests
from pymongo import MongoClient
from scrapy.selector import Selector

BASE_URL = 'https://eduardocavalcanti.com'
MONGO_URL = 'mongodb://localhost:27017/'
DB_NAME = 'tibia'


class BaseSpider:
    def __init__(self, login, password, base_url=BASE_URL, mongo_url=MONGO_URL, db_name=DB_NAME):
        self.mongo_client = MongoClient(mongo_url)
        self.db = self.mongo_client[db_name]
        self.base_url = base_url
        self.authenticated = False
        self.login = login
        self.password = password
        self.session = None

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

    def get_response(self, url):
        if not self.authenticated:
            self._authenticate()
        response = self.session.get(url)
        return Selector(text=response.text)

def extract_from_links(node):
    return dict(
        code=node.xpath('text()').get().strip(),
        url=node.attrib['href'],
    )
def extract_from_links(node, name='name'):
    return {
        name: node.xpath('text()').get().strip(),
        'url': node.attrib['href']
    }
