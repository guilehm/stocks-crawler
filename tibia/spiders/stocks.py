# -*- coding: utf-8 -*-
import scrapy

from selenium import webdriver
from scrapy.selector import Selector


class StocksSpider(scrapy.Spider):
    name = 'stocks'
    start_urls = ['https://eduardocavalcanti.com/dashboard/']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.driver = webdriver.Chrome('../../chromedriver')

    def parse(self, response):
        self.driver.get(response.url)
        email = 'vic.to.you@hotmail.com'
        password = 'Senhadovictor'
        name_input = self.driver.find_element_by_id('input_0')
        name_input.send_keys(email)
        password_input = self.driver.find_element_by_id('input_1')
        password_input.send_keys(password)
        button = self.driver.find_element_by_name('armFormSubmitBtn')
        button.submit()
        html = Selector(text=self.driver.page_source)

        def extract_from_links(node):
            return dict(
                code=node.xpath('text()').get().strip(),
                url=node.attrib['href'],
            )

        stocks = [extract_from_links(link) for link in html.xpath('//h2[@class="entry-title"]/a')]
        names = [name.strip() for name in html.xpath(
            '//article//div[@class="entry-content entry-summary"]//text()'
        ).getall() if name and name.strip()]
        [stock.update(name=name) for stock, name in list(zip(stocks, names))]
        yield [stock for stock in stocks]
        self.driver.close()
