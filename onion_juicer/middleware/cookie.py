from scrapy.downloadermiddlewares.cookies import CookiesMiddleware as BaseCookieMiddleware
from scrapy.exceptions import NotConfigured


class Cookie(BaseCookieMiddleware):

    KEY_DEFAULT = 'default'

    def __init__(self, debug=False, default=None):
        super().__init__(debug)
        if default is not None:
            z = self.jars[Cookie.KEY_DEFAULT]
            for i in default:
                z.jar.set_cookie(i)

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('COOKIES_ENABLED'):
            raise NotConfigured

        default = crawler.settings.get('COOKIES_DEFAULT')
        debug = crawler.settings.getbool('COOKIES_DEBUG')

        return cls(debug=debug) if not default else cls(debug=debug, default=default)
