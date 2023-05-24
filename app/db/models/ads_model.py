from tortoise import fields, models


class AdsModel(models.Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    description = fields.TextField(default="")
    show = fields.BooleanField(default=False)
    left_time = fields.DatetimeField()
    user = fields.ForeignKeyField("models.UserModel", on_delete=fields.CASCADE)

    class Meta:
        fields = '__all__'
