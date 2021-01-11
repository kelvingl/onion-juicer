from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy import Request
from .base_crawler import BaseCrawler


class WhiteHouseMarket(BaseCrawler):

    name = 'white_house_market'

    ignore_urls = []

    rules = (
        Rule(
            LinkExtractor(
                allow=[r'searchterm'],
                restrict_xpaths=['/html/body/div[4]/div/div/div[4]/div']
            ),
            process_request='request_page',
            follow=True
        ),
        Rule(
            LinkExtractor(
                allow=[r'action=show'],
                restrict_css=['html body div.container.listingsdiv div.row div.col-md-12 div.panel.panel-info div.panel-body']
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
        return self._setup_proxy(self._setup_cookies(request))

    def request_page(self, request, response=None):
        return self._request(request)

    def request_product(self, request, response=None):
        if not self._is_unique_result(request.url):
            return None
        return self._request(request)

    def parse_product(self, response):
        yield self._create_result({
            'title': response.xpath('/html/body/div[4]/div/div/div[3]/div[1]/strong/text()').get(),
            'price': float(response.xpath('/html/body/div[4]/div/div/div[3]/div[2]/div/div/div[3]/p[2]/text()').re_first('[^:]* (?:\\w{3}) ([^ ]*?) ').replace(',', '')),
            'description': response.xpath('/html/body/div[4]/div/div/div[4]/div[2]/textarea/text()').get(),
            'views': float(response.xpath('/html/body/div[4]/div/div/div[3]/div[2]/div/div/div[3]/p[6]/text()').re_first('Views: (.*)')),
            'url': response.url
        })

    def _prepare_start_url(self, url):
        z = super()._prepare_start_url(self, url)
        return 'http://' + z + '/welcome?searchterm=database&shipfrom=any&shipto=any&order_by_s=Newest+First&search=2'