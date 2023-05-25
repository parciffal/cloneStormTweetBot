from tortoise import fields, models


class AccountModel(models.Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    group = fields.ForeignKeyField("models.GroupModel", on_delete=fields.CASCADE)

    class Meta:
        fields = '__all__'
