from scrapy.spiders import CrawlSpider
from urllib.parse import urlparse
from onion_juicer.model import Result, Site
import datetime


class BaseCrawler(CrawlSpider):

    configs = {}
    _site = None
    ignore_urls = []
    allowed_domains = ['onion']

    def initialize_with_configs(self, configs):
        self.configs = configs

        self.start_urls = [self.configs.get('url', None)]

        self._site = self.configs.get('site', None)
        if self._site is None:
            raise ValueError('Site must be provided in configuration')

    def _set_user_agent(self, request):
        user_agent = self.configs.get('user_agent', 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0')
        request.headers['User-Agent'] = user_agent
        return request

    def _populate_cookies(self, request):
        cookies = self.configs.get('cookies', {})
        for k, v in cookies.items():
            request.cookies[k] = v
        return request

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
