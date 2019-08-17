import requests

BASE_URL = 'https://eduardocavalcanti.com'


class StockSpider:
    def __init__(self, login, password, base_url=BASE_URL):
        self.base_url = base_url
        self.authenticated = False
        self.login = login
        self.password = password
        self.session = None

    def _create_data_login(self):
        return {
            'action': 'arm_shortcode_form_ajax_action',
            'form_random_key': '102_06blAsIBsu',
            'user_login': self.login,
            'user_pass': self.password,
            'rememberme': '',
            'arm_action': 'please-login',
            'redirect_to': self.base_url,
            'isAdmin': '0',
            'referral_url': f'{self.base_url}/login/',
            'form_filter_kp': '9',
            'form_filter_st': '1566007996',
            'arm_nonce_check': '80161f9f45'
        }

    def _authenticate(self):
        session = requests.session()
        response = session.post(
            f'{self.base_url}/wp-admin/admin-ajax.php',
            data=self._create_data_login(),
        )
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
