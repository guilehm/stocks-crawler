# -*- coding: utf-8 -*-
import scrapy


class StocksSpider(scrapy.Spider):
    name = 'stocks'
    login_page = 'https://eduardocavalcanti.com/wp-admin/admin-ajax.php'
    handle_httpstatus_list = [500, 502, 400]
    start_urls = ['https://eduardocavalcanti.com/dashboard/']

    def parse(self, response):
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

        def stock_factory():
            return (stock for stock in stocks)

        yield from stock_factory()
