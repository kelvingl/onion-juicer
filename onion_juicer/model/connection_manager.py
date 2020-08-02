from peewee import MySQLDatabase
from .site import Site
from .result import Result


class ConnectionManager:
    tables = [Result, Site]
    _database = None
    _username = None
    _password = None
    _host = None
    _port = None
    _db_instance = None

    def __init__(self, database='onion', username='onion', password='onion', host='127.0.0.1', port=3306, drop_tables=False):
        self._database = database
        self._username = username
        self._password = password
        self._host = host
        self._port = port

        self.__instance_db()

        if drop_tables:
            self.__drop_schema()
        self.__create_schema()
        self._fake_data()

    def __instance_db(self):
        self._db_instance = MySQLDatabase(self._database,
                                          user=self._username,
                                          password=self._password,
                                          host=self._host,
                                          port=self._port)
        for i in self.tables:
            i.bind(self._db_instance)

    @staticmethod
    def _fake_data():
        Site.insert(slug='empire_market', name='Empire Market').execute()
        Site.insert(slug='icarus_market', name='Ikarus Market').execute()

    @staticmethod
    def __drop_schema():
        Result.drop_table()
        Site.drop_table()

    @staticmethod
    def __create_schema():
        Site.create_table()
        Result.create_table()
