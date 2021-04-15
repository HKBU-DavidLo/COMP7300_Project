from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.utils.timezone import now
from django.urls import reverse
from .forms import BuyShareForm
from .models import Transaction, Stock
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
import requests
import datetime
import logging
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
            
@login_required
def buy(request):
    page_title = 'Buy Form'
    form = BuyShareForm()
    symbol = 'AAPL'
    context = {
        'page_title': page_title,
        'form': form,
        'symbol': symbol,
    }
    return render(request, 'buy-order.html', context)

def getquote(request):
    symbol = request.GET.get('symbol', None) 
    token = 'c0n56cv48v6v1q0c1peg' # to be injected as env var
    r = requests.get('https://finnhub.io/api/v1/quote?symbol=' + symbol + '&token=' + token)
    data = r.json()
    return JsonResponse(data)

@login_required
def orderpreview(request):
    if request.method == 'POST':
        page_title = 'Preview Your Order'
        form = BuyShareForm(request.POST)
        if form.is_valid():
            context = {
                'form': form,
                'page_title': page_title, 
            }
            return render(request, 'order-preview.html', context)     
        else:
            pass

@login_required
def dashboard(request):
    cash = Cash.objects.get(user=request.user)
    username = request.user
    stocks = StockHoldings.objects.filter(user=request.user)
    stocks_update = []
    stock_update = {}
    total_pl = 0
    for stock in stocks:
        stock_update = {
            'symbol': stock.symbol,
            'quantity': stock.quantity,
            'avg_purchase_price': stock.avg_purchase_price
        }
        mkt_price = finnhub_client.quote(stock.symbol)['c']
        pl = (mkt_price - stock.avg_purchase_price)*stock.quantity
        stock_update['current'] = mkt_price
        stock_update['profit_loss'] = round(pl,2)
        stocks_update.append(stock_update)
        total_pl += round(pl, 2)
    context = {
        'username': username,
        'cash': cash.cash,
        'stocks': stocks_update,
        'total_pl': total_pl,
    }
    return render(request, 'dashboard.html', context)

@login_required
def confirmbuy(request):
    if request.method == 'POST':
        form = BuyShareForm(request.POST)
        if form.is_valid():
            try:
                stock_obj = Stock.objects.get(user=request.user, symbol=form.cleaned_data['stock'])
                stock_obj.bought_quantity = form.cleaned_data['quantity']
                position_before = stock_obj.long_position_after
                old_unit_price = stock_obj.bought_unit_price
                stock_obj.long_position_before = position_before
                stock_obj.long_position_after = position_before + form.cleaned_data['quantity'] 
                stock_obj.bought_unit_price = (position_before * old_unit_price + form.cleaned_data['quantity'] * form.cleaned_data['limit_price']) / stock_obj.long_position_after
                stock_obj.save()
                
            except Stock.DoesNotExist:
                stock_obj = Stock(
                    symbol=form.cleaned_data['stock'],
                    bought_quantity=form.cleaned_data['quantity'],
                    bought_unit_price=form.cleaned_data['limit_price'],
                    user=request.user,
                    long_position_after=form.cleaned_data['quantity'],
                )
                stock_obj.save()
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            return render(request, 'error.html', { 'form': form })