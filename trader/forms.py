from django import forms
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User

class BuyShareForm(forms.Form):
    SHARE_CHOICES = [
        ('Apple (AAPL)', 'AAPL'),
        ('Google (GOOG)', 'GOOG'),
        ('Yahoo (YHOO)', 'YHOO'),
        ('Amazon (AMZN)', 'AMZN'),
    ] 
    stock = forms.CharField(label='Select a stock', widget=forms.Select(choices=SHARE_CHOICES))
    quantity = forms.IntegerField(label='Quantity')
    limit_price = forms.IntegerField(label='Limit order price ($)')

    ## cleasing functions to be written
