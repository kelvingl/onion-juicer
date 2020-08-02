from peewee import MySQLDatabase
import os
import json
from .site import Site
from .result import Result


class ConnectionManager:
    tables = [Site, Result]
    _database = None
    _username = None
    _password = None
    _host = None
    _port = None
    _db_instance = None

    def __init__(self, database='onion', username='onion', password='onion', host='127.0.0.1', port=3306):
        self._database = database
        self._username = username
        self._password = password
        self._host = host
        self._port = port

        self.__instance_db()
        self.__drop_schema()
        self.__create_schema()
        self._fake_data()

    def _fake_data(self):
        Site.insert(slug='empire_market', name='Empire Market').execute()
        Site.insert(slug='icarus_market', name='Ikarus Market').execute()

    def __instance_db(self):
        self._db_instance = MySQLDatabase(self._database,
                                          user=self._username,
                                          password=self._password,
                                          host=self._host,
                                          port=self._port)
        for i in self.tables:
            i.bind(self._db_instance)

    def __drop_schema(self):
        for i in self.tables:
            i.drop_table()

    def __create_schema(self):
        for i in self.tables:
            i.create_table()
