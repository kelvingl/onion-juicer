from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy import Request
from scrapy import FormRequest
from math import ceil
from .base_crawler import BaseCrawler


class BigBlueMarket(BaseCrawler):

    name = 'big_blue_market'

    ignore_urls = []

    rules = (
        Rule(
            LinkExtractor(
                allow=[r'products'],
                restrict_css=['table.rid']
            ),
            process_request='request_product',
            follow=True,
            callback='parse_product'
        ),
    )

    def start_requests(self):
        for url in self.start_urls:
            yield self.request_page(Request(url=url, dont_filter=True, callback=self.do_search))

    def do_search(self, response):
        yield self.request_page(
            FormRequest.from_response(
                response,
                formid='my_form',
                formdata={
                    response.xpath('//form[@id="my_form"]//input[1]/@name').get(): 'database',
                    'newlis': 'newlis'
                },
                dont_filter=True,
                callback=self.iterate
            )
        )

    def iterate(self, response):
        for i in range(1, ceil(int(response.xpath('//div[@id="baggy"]/i/text()').re_first('(\d+)')) / 20)):
            yield self.request_page(
                FormRequest.from_response(
                    response,
                    formid='my_form',
                    formdata={
                        response.xpath('//form[@id="my_form"]//input[1]/@name').get(): 'database',
                        'newlis': 'newlis',
                        'page': str(i)
                    },
                    dont_filter=True
                )
            )

    def _request(self, request):
        return self._setup_proxy(self._setup_cookies(request))

    def request_page(self, request, response=None):
        return self._request(request)

    def request_product(self, request, response=None):
        if not self._is_unique_result(request.url):
            return None
        return self._request(request)

    def parse_product(self, response):
        yield self._create_result({
            'title': response.xpath('string(//div[@class="tittlos"]/text)').get().strip(),
            'price': float(response.css('.padp > span:nth-child(2)::text').re_first('(?:\\w{3}) (.*)').replace(',', '')),
            'description': response.xpath('string(//div[@id="textdesc"])').get().strip(),
            'views': None,
            'seller': response.css('.vendoritem > font:nth-child(1) > a:nth-child(1)::text').get().lower(),
            'url': response.url,
            'body': response.body
        })

    @staticmethod
    def _prepare_start_url(url):
        return 'http://' \
               + BaseCrawler._prepare_start_url(url) \
               + '/search/advanced/'
