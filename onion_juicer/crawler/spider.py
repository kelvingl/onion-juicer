from scrapy.spiders import CrawlSpider
from onion_juicer.model import Result


class Spider(CrawlSpider):

    configs = {}

    def initialize_with_configs(self, configs):
        self.configs = configs

        self.start_urls = [self.configs.get('url', None)]

    def _set_user_agent(self, request, callback=(lambda x: x)):
        user_agent = self.configs.get('user_agent', 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0')
        request.headers['User-Agent'] = user_agent
        return callback(request)

    def _populate_cookies(self, request, callback=(lambda x: x)):
        cookies = self.configs.get('cookie', {})
        for k, v in cookies:
            request.cookies[k] = v
        return callback(request)

    @staticmethod
    def _create_result(data):
        return Result.create(**data)

    @staticmethod
    def _is_unique_result(url):
        return Result.get_or_none(Result.url == url) is None
