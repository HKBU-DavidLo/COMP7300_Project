from django.shortcuts import render, get_object_or_404, redirect
import datetime
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .forms import BuyShareForm
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import Cash, StockHoldings
from django.template import loader
from django.shortcuts import render
import finnhub

# Setup client
finnhub_client = finnhub.Client(api_key="c0p7jnn48v6rvej4esog")

def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('dashboard'))
    else:
        return render(request, 'index.html')

def signup(request):
    pass

def orderpreview(request):
    pass

def signout(request):
    pass
            

def buy(request):
    username = 'Username'
    symbol = 'AAPL'
    context = {
        'username': username,
        'symbol': symbol,
    }
    return render(request, 'buy.html', context)

def buyorder(request):
    username = 'Username'
    symbol = 'AAPL'
    quote = 123.4
    context = {
        'username': username,
        'symbol': symbol,
        'quote': quote,
    }
    return render(request, 'buy-order.html', context)

def dashboard(request):
    cash = Cash.objects.get(user=request.user)
    username = request.user
    stocks = StockHoldings.objects.filter(user=request.user)
    stocks_update = []
    stock_update = {}
    for stock in stocks:
        stock_update = {
            'symbol': stock.symbol,
            'quantity': stock.quantity,
            'avg_purchase_price': stock.avg_purchase_price
        }
        stock_update['current'] = finnhub_client.quote(stock.symbol)['c']
        stocks_update.append(stock_update)
    context = {
        'username': username,
        'cash': cash.cash,
        'stocks': stocks_update,
    }
    return render(request, 'dashboard.html', context)