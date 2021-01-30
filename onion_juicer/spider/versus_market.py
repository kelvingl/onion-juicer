from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy import Request
from .base_crawler import BaseCrawler


class VersusMarket(BaseCrawler):

    name = 'versus_market'

    ignore_urls = []

    rules = (
        Rule(
            LinkExtractor(
                allow=[r'listing\/'],
                restrict_css=['.listings']
            ),
            process_request='request_product',
            follow=True,
            callback='parse_product'
        ),
        Rule(
            LinkExtractor(
                allow=[r'listing'],
                restrict_xpaths=['//div[@class="pagination"]/div[2]/a[3]']
            ),
            process_request='request_page',
            follow=True,
        ),
    )

    def start_requests(self):
        for url in self.start_urls:
            yield self.request_page(Request(url=url, dont_filter=True))

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
            'title': response.css('.listing__title > h1::text').get().strip(),
            'price': float(response.css('.currency::text').re_first('([^ ]+) (?:.*)').replace(',', '')),
            'description': response.xpath('string((//div[@class="listing__description"])//div[@class="tabs__content"])').get().strip(),
            'views': None,
            'sales': float(response.xpath('//div[@class="listing__product"]/table/tr[5]/td[2]/text()').get()),
            'seller':  response.xpath('//div[@class="listing__vendor"]/table/tr[1]/td[1]/strong/a/text()').get().lower(),
            'url': response.url,
            'body': response.body
        })

    @staticmethod
    def _prepare_start_url(url):
        return 'http://' \
               + BaseCrawler._prepare_start_url(url) \
               + '/listing?ipp=100&q=database&page=0'