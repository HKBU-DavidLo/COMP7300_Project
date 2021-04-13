from django.contrib import admin

# Register your models here.
from .models import Stock, Transaction, Cash, StockHoldings

admin.site.register(Stock)
admin.site.register(Transaction)
admin.site.register(Cash)
admin.site.register(StockHoldings)