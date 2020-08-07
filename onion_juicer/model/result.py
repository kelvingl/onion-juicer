from peewee import CharField, AutoField, TextField, DateTimeField, ForeignKeyField, FloatField
from .base_model import BaseModel
from .site import Site


class Result(BaseModel):
    id = AutoField(primary_key=True)
    title = CharField()
    price = FloatField()
    description = TextField()
    tags = TextField()
    url = CharField()
    date = DateTimeField()
    body = TextField()
    site = ForeignKeyField(Site)
