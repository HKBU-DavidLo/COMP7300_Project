from django.db import models
from django.contrib.auth.models import User
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
    created = models.DateField()
    updated = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


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

class Cash(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cash = models.FloatField()

class StockHoldings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    avg_purchase_price = models.FloatField()
    symbol = models.CharField(max_length=10)
