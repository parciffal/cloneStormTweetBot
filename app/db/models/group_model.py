from enum import IntEnum
from tortoise import fields, models


class TimeDelayEnum(IntEnum):
    FIVE = 5
    TEN = 10
    FIFTEEN = 15
    TWENTY = 20
    TWENTY_FIVE = 25
    THIRTY = 30
    THIRTY_FIVE = 35
    FORTY = 40
    FORTY_FIVE = 45
    FIFTY = 50
    FIFTY_FIVE = 55
    SIXTY = 60


class GroupModel(models.Model):
    telegram_id = fields.BigIntField(pk=True)
    name = fields.TextField(default="", max_length=255)
    comments = fields.TextField(default="")
    show_media = fields.BinaryField(null=True)
    media = fields.TextField(default="")
    delay = fields.IntEnumField(enum_type=TimeDelayEnum, default=TimeDelayEnum.FIVE)

    receiving_alerts = fields.BooleanField(default=False)
    influencers_tweets = fields.BooleanField(default=False)
    retweets_replies = fields.BooleanField(default=False)

    user = fields.ForeignKeyField("models.UserModel", on_delete=fields.CASCADE)

    class Meta:
        fields = '__all__'
