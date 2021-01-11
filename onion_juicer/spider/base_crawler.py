from scrapy.spiders import CrawlSpider
from urllib.parse import urlparse
from onion_juicer.model import Result, Site
import datetime


class BaseCrawler(CrawlSpider):

    configs = {}
    _site = None
    cookies = None
    ignore_urls = []
    allowed_domains = ['onion']

    def initialize_with_configs(self, configs):
        self.configs = configs

        self.start_urls = [self._prepare_start_url(self, self.configs.get('url', None))]

        self._site = self.configs.get('site', None)
        if self._site is None:
            raise ValueError('Site must be provided in configuration')

    def _import_cookies(self, filename):
        with open(filename) as h:
            self.cookies.set_cookie(h.readline())

    def _setup_proxy(self, request):
        proxy = self.configs.get('proxy', '')
        if proxy != '':
            request.meta['proxy'] = proxy
        return request

    def _setup_cookies(self, request):
        request.meta['cookiejar'] = 0

        if len(request.cookies) == 0:
            request.cookies = []
            for i in self.cookies:
                request.cookies.append({
                    "name": i.name,
                    "value": i.value,
                    "path": i.path,
                    "domain": i.domain
                })
        return request

    def _prepare_start_url(self, url):
        parse = urlparse(url)
        return parse.netloc or parse.path

    @staticmethod
    def _strip_url(url):
        url = urlparse(url)
        return f'{url.path}{"?" if url.query else ""}{url.query}'

    def _create_result(self, data):
        if 'url' in data:
            data['url'] = self._strip_url(data['url'])

        if data['url'] in self.ignore_urls:
            return None

        data['site'] = self._site
        data['date'] = datetime.datetime.now()
        Result.create(**data)

    def _is_unique_result(self, url):
        return Result \
            .select() \
            .join(Site) \
            .where(Result.url == self._strip_url(url), Site.id == self._site.id) \
            .count() == 0
