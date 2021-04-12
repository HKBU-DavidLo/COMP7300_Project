from django.shortcuts import render, get_object_or_404, redirect
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import BuyShareForm
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

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
    act_fund = 12410
    username = 'Username'
    context = {
        'username': username,
        'act_fund': act_fund,
    }
    return render(request, 'dashboard.html', context)