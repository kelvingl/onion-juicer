from peewee import AutoField, CharField
from .base_model import BaseModel


class Site(BaseModel):
    id = AutoField(primary_key=True)
    slug = CharField(unique=True)
    name = CharField()
