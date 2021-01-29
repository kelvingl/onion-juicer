import os
import yaml
import tempfile
from onion_juicer.model import ConnectionManager, Site as SiteModel
from onion_juicer.spider import Dark0deMarket
from onion_juicer.spider import WhiteHouseMarket
from scrapy.crawler import CrawlerProcess
from http.cookiejar import MozillaCookieJar


class OnionJuicer:

    _config = {}
    _spider_classes = [WhiteHouseMarket]
    _cm = None
    _crawler_process = None

    def __init__(self, config_path='%s/config.yaml' % os.getcwd()):
        self._config = yaml.safe_load(open(config_path))

    def extract(self):
        self._cm = self._create_connection_manager()

        all_sites = SiteModel.select()

        if len(all_sites) <= 0:
            return

        self._crawler_process = CrawlerProcess(self._get_crawler_process_settings())

        for _site in all_sites:
            _spider = self._create_spider(_site)
            if _spider is None:
                continue
            self._crawler_process.crawl(_spider)

        self._crawler_process.join()
        self._crawler_process.start()

    def _get_crawler_process_settings(self):
        throttle_config = self._config.get('throttle', {})
        return {
            'LOG_LEVEL': 'DEBUG',
            'ROBOTSTXT_OBEY': False,
            'AUTOTHROTTLE_ENABLED': throttle_config.get('enabled', False),
            'AUTOTHROTTLE_DEBUG': throttle_config.get('debug', False),
            'AUTOTHROTTLE_MAX_DELAY': 86400,
            'DOWNLOAD_DELAY': throttle_config.get('download_delay', 0),
            'CONCURRENT_REQUESTS': throttle_config.get('concurrent_requests', 8),
            'CONCURRENT_REQUESTS_PER_DOMAIN': throttle_config.get('concurrent_requests_per_domain', 8),
            'REDIRECT_ENABLED': False,
            'BOT_NAME': 'OnionJuicer',
            'COOKIES_ENABLED': True,
            'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0',
            'SPIDER_MODULES': list(set([z.__module__ for z in self._spider_classes])),
        }

    def _create_spider(self, site):
        site_configs = self._config.get('market_configs', {}).get(site.slug, {})

        site_configs['proxy'] = self._config.get('proxy', '')

        site_configs['site'] = site

        spider_class = None
        for c in self._spider_classes:
            if site.slug == c.name:
                spider_class = c

        if not site_configs.get('enabled', True):
            return

        if spider_class is None:
            return

        spider = self._crawler_process.spider_loader.load(spider_class.name)

        spider.initialize_with_configs(spider, site_configs)

        spider.cookies = self._create_cookiedict()

        return spider

    def _create_cookiedict(self):
        cookiejar = MozillaCookieJar()
        filename = self._config.get('cookiejar', None)
        if filename is None:
            return cookiejar

        # Solução de contorno
        tmpcookiefile = tempfile.NamedTemporaryFile(delete=False)
        tmpcookiefile.writelines([b"# HTTP Cookie File"])

        with open(filename) as f:
            for line in f:
                if line.startswith("#HttpOnly_"):
                    line = line[len("#HttpOnly_"):]
                tmpcookiefile.write(line.encode())
        tmpcookiefile.flush()
        tmpcookiefile.close()
        cookiejar = MozillaCookieJar()

        cookiejar.load(filename=tmpcookiefile.name, ignore_discard=True, ignore_expires=True)
        os.remove(tmpcookiefile.name)

        r = {}
        z = []
        for domain in cookiejar._cookies:
            if domain not in r:
                r[domain] = {}
            for path in cookiejar._cookies[domain]:
                if path not in r[domain]:
                    r[domain][path] = {}
                for cookiename in cookiejar._cookies[domain][path]:
                    r[domain][path][cookiename] = cookiejar._cookies[domain][path][cookiename]
                    z.append(cookiejar._cookies[domain][path][cookiename])

        return z

    def _create_connection_manager(self):
        db_config = self._config.get('database', {})

        database = db_config.get('name', 'onion')
        username = db_config.get('username', 'onion')
        password = db_config.get('password', 'onion')
        host = db_config.get('host', '127.0.0.1')
        port = db_config.get('port', 3306)
        drop_tables = db_config.get('drop_tables', False)

        return ConnectionManager(database=database, username=username, password=password, host=host, port=port, drop_tables=drop_tables)
