from tortoise import fields, models


class AdminModel(models.Model):
    telegram_id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=255, default="")
    show_adds = fields.BooleanField(default=True)

    class Meta:
        fields = '__all__'
