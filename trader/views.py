from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

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
    act_fund = 12410
    username = 'Username'
    context = {
        'username': username,
        'act_fund': act_fund,
    }
    return render(request, 'dashboard.html', context)