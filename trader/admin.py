from django.contrib import admin
from .models import Transaction, Stock
# Register your models here.
admin.site.register(Stock)
admin.site.register(Transaction)