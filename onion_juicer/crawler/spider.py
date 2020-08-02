from scrapy.spiders import CrawlSpider
from urllib.parse import urlparse
from onion_juicer.model import Result


class Spider(CrawlSpider):

    configs = {}
    site_id = None

    def initialize_with_configs(self, configs):
        self.configs = configs

        self.start_urls = [self.configs.get('url', None)]
        self.site_id = self.configs.get('site_id', None)


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
        Result.create(**data)

    def _is_unique_result(self, url):
        return Result.get_or_none(Result.url == self._strip_url(url)) is None
