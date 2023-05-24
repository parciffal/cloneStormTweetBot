from tortoise import fields, models


class UserModel(models.Model):
    telegram_id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=255, default="")

    class Meta:
        fields = '__all__'
