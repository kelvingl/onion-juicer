from scrapy.spiders import CrawlSpider
from onion_juicer.model import Result


class Spider(CrawlSpider):

    configs = {}

    @classmethod
    def initialize_with_configs(cls, configs):
        cls.start_urls = configs.get('url', None)

    @classmethod
    def _set_user_agent(cls, request, callback=(lambda x: x)):
        user_agent = cls.configs.get('user_agent', 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0')
        request.headers['User-Agent'] = user_agent
        return callback(request)

    @classmethod
    def _populate_cookies(cls, request, callback=(lambda x: x)):
        cookies = cls.configs.get('cookie', {})
        for k, v in cookies:
            request.cookies[k] = v
        return callback(request)

    @classmethod
    def _create_result(cls, data):
        return Result.create(**data)

    @classmethod
    def _is_unique_result(cls, url):
        return Result.get_or_none(Result.url == url) is None
