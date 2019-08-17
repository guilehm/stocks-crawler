class StockSpider:
    def __init__(self, url, login, password):
        self.url = url
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
            'redirect_to': 'https://eduardocavalcanti.com',
            'isAdmin': '0',
            'referral_url': 'https://eduardocavalcanti.com/login/',
            'form_filter_kp': '9',
            'form_filter_st': '1566007996',
            'arm_nonce_check': '80161f9f45'
        }

