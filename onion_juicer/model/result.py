from peewee import CharField, AutoField, TextField, DateTimeField, ForeignKeyField, FloatField
from .base_model import BaseModel
from .site import Site


class Result(BaseModel):
    id = AutoField(primary_key=True)
    title = CharField()
    price = FloatField()
    views = FloatField(null=True)
    seller = FloatField(null=True)
    description = TextField()
    tags = TextField(null=True)
    url = CharField()
    date = DateTimeField()
    body = TextField(null=True)
    site = ForeignKeyField(Site)
