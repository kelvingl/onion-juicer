from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy import Request
from .spider import Spider
import datetime


class IcarusMarket(Spider):

    name = 'icarus_market'
    allowed_domains = ['onion']
    start_urls = []

    rules = (
        Rule(
            LinkExtractor(
                allow=[r'/search/'],
                restrict_css=['ul.pagination li']
            ),
            process_request='request_page',
            follow=True
        ),
        Rule(
            LinkExtractor(
                allow=[r'/listing/'],
                restrict_css=['.table']
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
            'title': response.xpath('/html/body/div/div/main/div[2]/div[2]/div[2]/div/div[1]/i[1]/text()').get(),
            'price': float(response.css('/html/body/div/div/main/div[2]/div[2]/div[2]/b[1]/following-sibling::text()[1]').re_first('(?:^ ) (.*)')),
            'description': response.css('textarea.form-control::text').get(),
            'tags': response.css('div.tabcontent div.tagsDiv span.tags a::text').getall(),
            'url': response.url,
            'body': response.body,
        })
