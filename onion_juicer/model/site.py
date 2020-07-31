import json
from peewee import AutoField, CharField
from .base_model import BaseModel


class Site(BaseModel):
    id = AutoField(primary_key=True)
    slug = CharField(unique=True)
    name = CharField()

    _url = None

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, obj):
        self._url = obj

    _cookie = {}

    @property
    def cookie(self):
        return self._cookie

    @cookie.setter
    def cookie(self, obj):
        _obj = obj
        if type(obj) == 'string':
            _obj = json.loads(obj)
        self._cookie = _obj
