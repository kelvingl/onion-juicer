from peewee import CharField, AutoField, TextField, DateTimeField, ForeignKeyField, FloatField
from .base_model import BaseModel
from .site import Site


class Result(BaseModel):
    id = AutoField(primary_key=True)
    title = CharField()
    price = FloatField()
    views = FloatField(null=True, default=0)
    sales = FloatField(null=True, default=0)
    seller = TextField(null=True, default=None)
    description = TextField()
    tags = TextField(null=True, default=None)
    url = CharField()
    date = DateTimeField()
    body = TextField(null=True, default=None)
    site = ForeignKeyField(Site)
