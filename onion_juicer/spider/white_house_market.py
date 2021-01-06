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

    def request_product(self, request):
        if not self._is_unique_result(request.url):
            return None
        return self._request(request)

    def parse_product(self, response):
        yield self._create_result({
            'title': response.xpath('/html/body/div/div/main/div[2]/div[2]/div[2]/div/div[1]/i[1]/text()').get(),
            'price': float(response.xpath('/html/body/div/div/main/div[2]/div[2]/div[2]/b[1]/following-sibling::text()[1]').re_first('(?:[^ ]+) (.*) ').replace(',', '')),
            'description': response.css('textarea.form-control::text').get(),
            'url': response.url,
            'body': response.body
        })

    def _prepare_start_url(self, url):
        z = super()._prepare_start_url(self, url)
        return 'http://' + z + '/welcome?searchterm=database&shipfrom=any&shipto=any&order_by_s=Newest+First&search=2'