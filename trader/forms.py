from django import forms
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User

class BuyShareForm(forms.Form):
    SHARE_CHOICES = [
        ('AAPL', 'Apple (AAPL)'),
        ('GOOG', 'Google (GOOG)'),
        ('BUD', 'AB InBev (ABI)'),
        ('AMZN', 'Amazon (AMZN)'),
        ('BTI', 'BA Tobacco (BTI)'),
        ('ET', 'Energy Transfer (ET)'),
        ('NI', 'NiSource (NI)'),
    ] 
    stock = forms.ChoiceField(label='Select a stock', choices=SHARE_CHOICES)
    quantity = forms.IntegerField(label='Quantity')
    limit_price = forms.FloatField(label='Limit order price (US$)')
    tx_time = forms.DateField(widget=forms.HiddenInput(), required=False)

    ## cleasing functions to be written

class DepositCashForm(forms.Form):
    cash = forms.FloatField(label='Amount of cash to be deposited')
    tx_time = forms.DateField(widget=forms.HiddenInput(), required=False)