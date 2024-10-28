from tortoise import models, fields


class BaseModel(models.Model):
    """Базовая модель."""

    id = fields.IntField(primary_key=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True
