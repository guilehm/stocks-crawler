# -*- coding: utf-8 -*-
import scrapy


class StocksSpider(scrapy.Spider):
    name = 'stocks'
    allowed_domains = ['https://eduardocavalcanti.com/dashboard/']
    start_urls = ['http://https://eduardocavalcanti.com/dashboard//']

    def parse(self, response):
        pass
