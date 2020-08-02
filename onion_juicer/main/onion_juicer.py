import os
import yaml
from onion_juicer.model import ConnectionManager, Site as SiteModel
from onion_juicer.crawler import EmpireMarket, IcarusMarket
from scrapy.crawler import CrawlerProcess


class OnionJuicer:

    _config = {}
    _spider_classes = [EmpireMarket, IcarusMarket]
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
        return {
            'LOG_LEVEL': 'DEBUG',
            'ROBOTSTXT_OBEY': False,
            'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
            'REDIRECT_ENABLED': False,
            'BOT_NAME': 'OnionJuicer',
            'SPIDER_MODULES': list(set([z.__module__ for z in self._spider_classes])),
        }

    def _create_spider(self, site):
        site_configs = self._config.get('market_configs', {}).get(site.slug, {})

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

        return spider

    def _create_connection_manager(self):
        db_config = self._config.get('database', {})

        database = db_config.get('name', 'onion')
        username = db_config.get('username', 'onion')
        password = db_config.get('password', 'onion')
        host = db_config.get('host', '127.0.0.1')
        port = db_config.get('port', 3306)
        drop_tables = db_config.get('drop_tables', False)

        return ConnectionManager(database=database, username=username, password=password, host=host, port=port, drop_tables=drop_tables)
