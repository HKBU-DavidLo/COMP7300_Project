from django.db import models
from django.db.models import UniqueConstraint
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
# Create your models here.

class Stock(models.Model):
    symbol = models.CharField(max_length=10)
    bought_quantity = models.IntegerField(default=0)
    bought_unit_price = models.FloatField(default=0.0)
    sold_quantity = models.IntegerField(default=0)
    sold_unit_price = models.FloatField(default=0.0)
    long_position_before = models.IntegerField(default=0)
    long_position_after = models.IntegerField(default=0)
    short_position_before = models.IntegerField(default=0)
    short_position_after = models.IntegerField(default=0)
    created = models.DateTimeField(editable=False)
    updated = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super(Stock, self).save(*args, **kwargs)

    class Meta:
        # ensure one user can own same stock once
        UniqueConstraint(fields=['symbol', 'user'], name='unique_holding')


class Transaction(models.Model):
    TX_TYPE = (
        ('b', 'buy'),
        ('s', 'sell'),
    )
    tx_type = models.CharField(max_length=1, choices=TX_TYPE, verbose_name="transaction type")
    stock = models.OneToOneField(Stock, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()
    unit_price = models.FloatField()
    tx_time = models.DateField(verbose_name="transction time")
    fee = models.FloatField(verbose_name="transaction fee", null=True)
    tax = models.FloatField(verbose_name="tax levied", null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
