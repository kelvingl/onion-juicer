from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy import Request
from main.service import Onion as OnionService
from .spider import Spider
import json
import datetime


class EmpireMarket(Spider):

    name = 'empire'
    allowed_domains = ['onion']

    cookie = {}

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

    def __init__(self, *args, **kwargs):
        super(EmpireMarket, self).__init__(*args, **kwargs)

        self.o_service = OnionService()

        self.start_urls = self.o_service.get_sites()

    def start_requests(self):
        for z, site in enumerate(self.start_urls):
            request = Request(url=site.url, dont_filter=True)
            self.cookie = json.loads(site.cookies).items()
            yield self.request_page(request)

    def _request(self, request):
        request.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0'

        for k, v in self.cookie:
            request.cookies[k] = v

        return request

    def request_page(self, request):
        return self._request(request)

    def request_product(self, request):
        if not self.o_service.is_url_unique(request.url):
            return None
        return self._request(request)

    def parse_product(self, response):
        yield self.o_service.create_result({
            'title': response.css('div.listDes h2::text').get(),
            'price': response.css('form p.padp span::text').get(),
            'description': response.css('div.tabcontent p::text').get(),
            'tags': response.css('div.tabcontent div.tagsDiv span.tags a::text').getall(),
            'url': response.url,
            'body': response.body,
            'timestamp': datetime.datetime.now()
        })
