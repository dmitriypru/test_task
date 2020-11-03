from tortoise import fields, models


class Rate(models.Model):
    id = fields.IntField(pk=True)
    date = fields.DateField(description='Date')
    cargo_type = fields.TextField(description='Cargo type')
    rate = fields.FloatField(description='Rate')

    class Meta:
        table = "rate"

    def __str__(self):
        return self.name
