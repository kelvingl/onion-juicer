from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy import Request
from .spider import Spider
import datetime


class EmpireMarket(Spider):

    name = 'empire_market'
    allowed_domains = ['onion']
    start_urls = []

    rules = (
        Rule(
            LinkExtractor(
                allow=[r'/searchproducts/'],
                restrict_css=['ul.pagination li']
            ),
            process_request='request_page',
            follow=True
        ),
        Rule(
            LinkExtractor(
                allow=[r'/product/'],
                restrict_css=['.col-1search']
            ),
            process_request='request_product',
            follow=True,
            callback='parse_product'
        ),
    )

    def start_requests(self):
        for url in self.start_urls:
            yield self.request_page(Request(url=url, dont_filter=True))

    def _request(self, request):
        return self._set_user_agent(self._populate_cookies(request))

    def request_page(self, request):
        return self._request(request)

    def request_product(self, request):
        if not self._is_unique_result(request.url):
            return None
        return self._request(request)

    def parse_product(self, response):
        yield self._create_result({
            'title': response.css('div.listDes h2::text').get(),
            'price': float(response.css('form p.padp span::text').re_first('USD (.*)').replace(',', '')),
            'description': response.css('div.tabcontent p::text').get(),
            'tags': response.css('div.tabcontent div.tagsDiv span.tags a::text').getall(),
            'url': response.url
        })
