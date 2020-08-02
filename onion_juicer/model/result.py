from peewee import CharField, AutoField, TextField, BigIntegerField
from .base_model import BaseModel


class Result(BaseModel):
    id = AutoField(primary_key=True)
    title = CharField()
    price = CharField()
    description = TextField()
    tags = TextField()
    url = CharField(unique=True)
    timestamp = BigIntegerField()
