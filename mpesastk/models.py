from django.db import models
from django.core.validators import MinValueValidator


# Create your models here.
class AbstractBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ResponseBody(AbstractBaseModel):
    body = models.JSONField()


class Transacton(AbstractBaseModel):
    phone_number = models.CharField(max_length=15)
    amount = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    receipt_number = models.CharField(max_length=100)

    def __str__(self):
        return self.receipt_number