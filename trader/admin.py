from django.contrib import admin
from .models import Stock, Transaction, Cash, StockHoldings

admin.site.register(Stock)
admin.site.register(Transaction)
admin.site.register(Cash)
admin.site.register(StockHoldings) 
