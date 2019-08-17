# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest, JSONRequest
from scrapy.utils.spider import iterate_spider_output
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError

class StocksSpider(scrapy.Spider):
    name = 'stocks'
    login_page = 'https://eduardocavalcanti.com/wp-admin/admin-ajax.php'
    # login_page = 'https://eduardocavalcanti.com/login/'
    handle_httpstatus_list = [500, 502, 400]
    start_urls = ['https://eduardocavalcanti.com/dashboard/']

    def start_requests(self):
        """This function is called before crawling starts."""
        # return [JSONRequest(url=self.login_page, callback=self.login, method='POST', data=data)]
        return [Request(url=self.login_page, callback=self.login)]
        # return [JSONRequest(url=self.login_page, data=data)]

    def login(self, response):
        """Generate a login request."""
        print('vai tentar logar ** -- ** -- ')
        print('vai tentar logar ** -- ** -- ')
        print('vai tentar logar ** -- ** -- ')
        data = {
            'action': 'arm_shortcode_form_ajax_action',
            'form_random_key': '102_06blAsIBsu',
            'user_login': 'vic.to.you@hotmail.com',
            'user_pass': 'Senhadovictor',
            'rememberme': '',
            'arm_action': 'please-login',
            'redirect_to': 'https://eduardocavalcanti.com',
            'isAdmin': '0',
            'referral_url': 'https://eduardocavalcanti.com/login/',
            'form_filter_kp': '9',
            'form_filter_st': '1566007996',
            'arm_nonce_check': '80161f9f45'
        }
        # return self.parse(response)
        return FormRequest.from_response(
            response,
            formname='arm_form',
            formdata=data,
            callback=self.check_login_response
        )
        # url = 'https://eduardocavalcanti.com/wp-admin/admin-ajax.php'
        # return Request(url=url, method='POST', data=data, callback=self.check_login_response)

    # def init_request(self):
    #     """This function is called before crawling starts."""
    #     print('chamou init_request ** -- ** ')
    #     print('chamou init_request ** -- ** ')
    #     print('chamou init_request ** -- ** ')
    #     print('chamou init_request ** -- ** ')
    #     print('chamou init_request ** -- ** ')
    #     data = {
    #         'action': 'arm_shortcode_form_ajax_action',
    #         'form_random_key': '102_06blAsIBsu',
    #         'user_login': 'vic.to.you@hotmail.com',
    #         'user_pass': 'Senhadovictor',
    #         'rememberme': '',
    #         'arm_action': 'please-login',
    #         'redirect_to': 'https://eduardocavalcanti.com',
    #         'isAdmin': '0',
    #         'referral_url': 'https://eduardocavalcanti.com/login/',
    #         'form_filter_kp': '9',
    #         'form_filter_st': '1566007996',
    #         'arm_nonce_check': '80161f9f45'
    #     }
    #     Request(url=self.login_page, method='POST')
    #
    #     return Request(url=self.login_page, callback=self.start_requests, method='POST')
    #
    # def start_requests(self, *args, **kwargs):
    #     self._postinit_reqs = super().start_requests()
    #     return iterate_spider_output(self.init_request())
    #
    #
    def initialized(self, response=None):
        """This method must be set as the callback of your last initialization
        request. See self.init_request() docstring for more info.
        """
        print('chamou initialized ** -- ** ')
        print('chamou initialized ** -- ** ')
        print('chamou initialized ** -- ** ')
        return self.__dict__.pop('_postinit_reqs', '')
    #
    # def start_requests(self):
    #     print("\n start_request is here \n")
    #     print("\n start_request is here \n")
    #     print("\n start_request is here \n")
    #     print("\n start_request is here \n")
    #     print("\n start_request is here \n")
    #     print("\n start_request is here \n")
    #     yield Request(
    #         url=self.login_page,
    #         callback=self.login,
    #         dont_filter=True
    #     )

    # def login(self, response):
    #     print('******** login **********\n' * 40 )
    #     if response.status == 400:
    #         print('deu erro')
    #         print(response)
    #         print(dir(response))
    #         return
    #     data = {
    #         'action': 'arm_shortcode_form_ajax_action',
    #         'form_random_key': '102_06blAsIBsu',
    #         'user_login': 'vic.to.you@hotmail.com',
    #         'user_pass': 'Senhadovictor',
    #         'rememberme': '',
    #         'arm_action': 'please-login',
    #         'redirect_to': 'https://eduardocavalcanti.com',
    #         'isAdmin': '0',
    #         'referral_url': 'https://eduardocavalcanti.com/login/',
    #         'form_filter_kp': '9',
    #         'form_filter_st': '1566007996',
    #         'arm_nonce_check': '80161f9f45'
    #     }
    #     return FormRequest.from_response(
    #         response,
    #         formdata=data,
    #         callback=self.check_login_response,
    #         # callback=self.parse,
    #     )

    def check_login_response(self, response):
        print('vai testar e chamar initialized')
        print('vai testar e chamar initialized')
        print('vai testar e chamar initialized')
        # print(type(response.body))
        # print(response.body)
        # print(type(response.body))
        # print('vai testar')
        # if 'title="TELB"' in str(response.body):
        #     self.log("Successfully logged in. Let's start crawling!")
        return self.parse(response)

        # self.log("Bad times :(")
        # self.log("Something went wrong, we couldn't log in, so nothing happens.")

    def parse(self, response):
        print('chegou no parse')
        def extract_from_links(node):
            return dict(
                code=node.xpath('text()').get().strip(),
                url=node.attrib['href'],
            )
        stocks = [extract_from_links(link) for link in response.xpath('//h2[@class="entry-title"]/a')]
        names = [name.strip() for name in response.xpath(
            '//article//div[@class="entry-content entry-summary"]//text()'
        ).getall() if name and name.strip()]
        [stock.update(name=name) for stock, name in list(zip(stocks, names))]
        print(stocks)
        print(response)

        def stock_factory():
            return (stock for stock in stocks)
        yield from stock_factory()
