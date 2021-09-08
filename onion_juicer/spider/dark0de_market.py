from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy import Request
from time import sleep
from .base_crawler import BaseCrawler


class Dark0deMarket(BaseCrawler):

    name = 'dark0de_market'

    ignore_urls = []

    product_details = {}

    rules = (
        Rule(
            LinkExtractor(
                allow=[r'search'],
                restrict_xpaths=['(//div[@class="news_navigation"])/ul/li[3]/a']
            ),
            process_request='request_page',
            follow=True,
            callback='parse_page'
        ),
        Rule(
            LinkExtractor(
                allow=[r'/product/'],
                restrict_css=['.top-products']
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

    def parse_page(self, response):
        for item in response.css('.top-products .miniview-container'):
            key = item.css('.product-name a:first-of-type::attr(href)').get()
            views = int(item.css('li.eye::text').get())
            sales = int(item.css('li.tag::text').get())
            self.product_details[key] = {'views': views, 'sales': sales}

    def parse_product(self, response):
        url = self._strip_url(response.url)
        while url not in self.product_details:
            sleep(1)
        product_details = self.product_details[url] if url in self.product_details else {}
        views = float(product_details.get('views', 0))
        sales = float(product_details.get('sales', 0))
        yield self._create_result({
            'title': response.css('h3.product-name::text').get(),
            'description': response.css('div.product-detail xmp:first-of-type::text').get(),
            'seller': response.xpath('//div[@class="product-detail"]/ul/li[1]/b/a/text()').get().lower(),
            'price': float(response.xpath('(//i[contains(@class, "fa-usd")])[1]/following-sibling::text()').get().replace(',', '')),
            'views': views,
            'sales': sales,
            'url': response.url,
            'body': response.body
        })

    @staticmethod
    def _prepare_start_url(url):
        url = BaseCrawler._prepare_start_url(url)
        return 'http://' \
               + BaseCrawler._prepare_start_url(url) \
               + '/search/Database/all/1?stype=All&sorigin=All&svendor=All&sdeaddrop=All&sortby=Price+asc&searchterm=&minprice=0&maxprice=99999'
