import datetime
from enum import Enum

from tortoise import fields, models


class LeftTime(Enum):
    DAY = datetime.timedelta(1)
    WEEK = datetime.timedelta(7)
    MONTH = datetime.timedelta(30)
    YEAR = datetime.timedelta(365)


class AdsModel(models.Model):
    id = fields.IntField(pk=True)
    name = fields.TextField(default="")
    description = fields.TextField(default="")
    media = fields.TextField(default="")
    comment_add = fields.BooleanField(default=False)
    show = fields.BooleanField(default=False)
    left_time = fields.DatetimeField(default=datetime.datetime.now()+datetime.timedelta(7))
    admin = fields.ForeignKeyField("models.AdminModel", on_delete=fields.CASCADE)

    class Meta:
        fields = '__all__'

