import os
import yaml
from onion_juicer.model import ConnectionManager, Site as SiteModel
from onion_juicer.crawler import EmpireMarket
import sys


class OnionJuicer:

    _config = {}
    _spider_classes = [EmpireMarket]
    _cm = None

    def __init__(self,
                 config_path='%s/config.yaml' % os.getcwd()):
        self._config = yaml.safe_load(open(config_path))

    @classmethod
    def extract(cls):
        cls._cm = cls._create_connection_manager()

        all_sites = SiteModel.select()

        if len(all_sites) <= 1:
            return

        spiders = []
        for _site in all_sites:
            _spider = cls._create_spider(_site)
            if _spider is None:
                continue
            spiders.append(_spider)

        sys.exit(1)

    @classmethod
    def _create_spider(cls, site):
        site_configs = cls._config.get('market_configs', {}).get(site.slug, {})

        spider_class = None
        for c in cls._spider_classes:
            if site.slug == c.name:
                spider_class = c

        if not site_configs.get('enabled', True):
            return

        if spider_class is None:
            return

        spider = spider_class()

        spider.initialize_with_configs(site_configs)

        return spider

    @classmethod
    def _create_connection_manager(cls):
        db_config = cls._config.get('database', {})

        database = db_config.get('name', 'onion')
        username = db_config.get('username', 'onion')
        password = db_config.get('password', 'onion')
        host = db_config.get('host', '127.0.0.1')
        port = db_config.get('port', 3306)

        return ConnectionManager(database=database, username=username, password=password, host=host, port=port)
