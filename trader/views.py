from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.utils.timezone import now
from django.urls import reverse
from .forms import ShareTransactionForm, DepositCashForm, WithdrawCashForm
from .models import Transaction, Stock, Cash, CashTX
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
import requests
import datetime
import logging
from .models import Cash
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

def signout(request):
    pass
            
@login_required
def buy(request):
    page_title = 'Buy Share Form'
    form = ShareTransactionForm()
    context = {
        'page_title': page_title,
        'form': form,
        'action': 'buyorder-preview',
    }
    return render(request, 'share-order.html', context)

@login_required
def sell(request):
    page_title = 'Sell Share Form'
    form = ShareTransactionForm()
    context = {
        'page_title': page_title,
        'form': form,
        'action': 'sellorder-preview',
    }
    return render(request, 'share-order.html', context)

@login_required
def sellorderpreview(request):
    if request.method == 'POST':
        page_title = 'Preview Your Oder'
        form = ShareTransactionForm(request.POST)
        if form.is_valid():
            symbol = form.cleaned_data['stock']
            try:
                stock_obj = Stock.objects.get(user=request.user, symbol=form.cleaned_data['stock'])
                shares_owned = stock_obj.long_position_after
                quantity = form.cleaned_data['quantity']
                if quantity > shares_owned:
                    error_msg = "You don't have sufficient stocks to sell, please re-try."
                    form = ShareTransactionForm()
                    context = {
                        'form': form,
                        'page_title': error_msg,
                        'error_msg': error_msg,
                        'action': 'sellorder-preview',
                    }
                    return render(request, 'share-order.html', context)
                context = {
                    'form': form,
                    'page_title': page_title, 
                }
                return render(request, 'sellorder-preview.html', context) 
            except Stock.DoesNotExist:
                error_msg = "You don't own this stock, short-selling is currently not supported."
                form = ShareTransactionForm()
                context = {
                    'form': form,
                    'page_title': 'No Stock Owned',
                    'error_msg': error_msg,
                    'action': 'sellorder-preview',
                }
                return render(request, 'share-order.html', context)
    else:
        pass

def getquote(request):
    symbol = request.GET.get('symbol', None) 
    token = 'c0n56cv48v6v1q0c1peg' # to be injected as env var
    r = requests.get('https://finnhub.io/api/v1/quote?symbol=' + symbol + '&token=' + token)
    data = r.json()
    return JsonResponse(data)

@login_required
def buyorderpreview(request):
    if request.method == 'POST':
        page_title = 'Preview Your Order'
        form = ShareTransactionForm(request.POST)
        if form.is_valid():
            cash = float(Cash.objects.get(user=request.user))
            quantity = form.cleaned_data['quantity']
            price = form.cleaned_data['limit_price']
            fee = quantity * price * 0.005 # assume commission of 0.5%
            cash_required = quantity * price + fee
            if cash > cash_required:
                context = {
                    'form': form,
                    'page_title': page_title, 
                }
                return render(request, 'buyorder-preview.html', context)     
            else:
                form = ShareTransactionForm()
                context = {
                    'form': form,
                    'page_title': 'Insufficient Fund',
                    'action': 'buyorder-preview',
                    'error_msg': "You don't have enough cash, please deposit and try again!",
                }
                return render(request, 'share-order.html', context)
        else:
            pass

@login_required
def dashboard(request):
    cash = float(Cash.objects.get(user=request.user))
    username = request.user
    stocks = Stock.objects.filter(user=request.user)
    stocks_update = []
    stock_update = {}
    total_pl = 0
    total_mkt_value = 0
    total_acct_value = 0
    for stock in stocks:
        stock_update = {
            'symbol': stock.symbol,
            'quantity': stock.long_position_after,
            'avg_purchase_price': stock.bought_unit_price
        }
        mkt_price = finnhub_client.quote(stock.symbol)['c']
        pl = (mkt_price - stock.bought_unit_price)*stock.bought_quantity
        mkt_val = mkt_price * stock.bought_quantity
        stock_update['current'] = mkt_price
        stock_update['profit_loss'] = round(pl,2)
        stocks_update.append(stock_update)
        total_pl += round(pl, 2)
        total_mkt_value += round(mkt_val, 2)
    total_acct_value = total_mkt_value + cash
    context = {
        'username': username,
        'cash': cash,
        'stocks': stocks_update,
        'total_pl': total_pl,
        'total_mkt_value': total_mkt_value,
        'total_acct_value': total_acct_value
    }
    return render(request, 'dashboard.html', context)

@login_required
def confirmbuy(request):
    if request.method == 'POST':
        form = ShareTransactionForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            price = form.cleaned_data['limit_price']
            fee = quantity * price * 0.005 # assume 0.5% commission for the moment
            tax = 0.0 # assume no tax for the moment
            cash_required = quantity * price + fee
            cash_obj = get_object_or_404(Cash, user=request.user)
            cash_obj.cash -= cash_required
            
            try:
                stock_obj = Stock.objects.get(user=request.user, symbol=form.cleaned_data['stock'])
                stock_obj.bought_quantity = quantity
                position_before = stock_obj.long_position_after
                old_unit_price = stock_obj.bought_unit_price
                stock_obj.long_position_before = position_before
                stock_obj.long_position_after = position_before + quantity
                stock_obj.bought_unit_price = (position_before * old_unit_price + quantity * price) / stock_obj.long_position_after
                stock_obj.save()
                cash_obj.save()
                
            except Stock.DoesNotExist:
                stock_obj = Stock(
                    symbol=form.cleaned_data['stock'],
                    bought_quantity=quantity,
                    bought_unit_price=price,
                    user=request.user,
                    long_position_after=quantity,
                )
                stock_obj.save()
                cash_obj.save()
            tx_object = Transaction(
                tx_type='b',
                symbol=form.cleaned_data['stock'],
                quantity=quantity,
                unit_price=price,
                fee=fee, 
                tax=tax, 
                tx_time=stock_obj.updated,
                user=request.user,
            )
            tx_object.save()
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            return render(request, 'error.html', { 'form': form })

@login_required
def confirmsell(request):
    if request.method == "POST":
        form = ShareTransactionForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            price = form.cleaned_data['limit_price']
            fee = quantity * price * 0.005 #assume 0.5% commission for the moment
            tax = 0.0 # assume no tax for the moment
            proceeds = quantity * price - fee
            cash_obj = get_object_or_404(Cash, user=request.user)
            cash_obj.cash += proceeds
            try:
                stock_obj = Stock.objects.get(user=request.user, symbol=form.cleaned_data['stock'])
                stock_obj.sold_quantity = quantity
                original_cost = stock_obj.long_position_after * stock_obj.bought_unit_price
                stock_obj.long_position_before = stock_obj.long_position_after
                stock_obj.long_position_after = stock_obj.long_position_after - quantity
                #update the remaining shares' unit cost 
                new_original_cost = original_cost - quantity * price
                if new_original_cost < 0:
                    stock_obj.bought_unit_price = 0.0
                else:
                    stock_obj.bought_unit_price = new_original_cost / stock_obj.long_position_after
                stock_obj.save()
                cash_obj.save()
                tx_object = Transaction(
                    tx_type='s',
                    symbol=form.cleaned_data['stock'],
                    quantity=quantity,
                    unit_price=price,
                    fee=fee,
                    tax=tax,
                    tx_time=stock_obj.updated,
                    user=request.user
                )
                tx_object.save()
                return HttpResponseRedirect(reverse('dashboard'))
            except Stock.DoesNotExist:
                return render(request, 'error.html')
    else:
        pass

@login_required
def depositcash(request):
    page_title = 'Form for depositing cash'
    cash = float(Cash.objects.get(user=request.user))
    username = request.user
    form = DepositCashForm()
    context = {
        'cash': cash,
        'username': username,
        'form': form,
        'action': 'deposit',
        'resource': 'deposit-preview',
        'page_title': page_title,
    }
    return render(request, 'cash-action.html', context)

@login_required
def depositpreview(request):
    if request.method == 'POST':
        page_title = 'Preview Your Instruction to Deposit'
        form = DepositCashForm(request.POST)
        if form.is_valid():
            context = {
                'form': form,
                'page_title': page_title, 
            }
            return render(request, 'deposit-preview.html', context)     
        else:
            pass

@login_required
def confirmdeposit(request):
    if request.method == 'POST':
        form = DepositCashForm(request.POST)
        if form.is_valid():
            cash = form.cleaned_data['cash']
            cash_obj = get_object_or_404(Cash, user=request.user)
            cash_before = cash_obj.cash
            cash_obj.cash += cash
            cash_obj.save()
                
            
            cashtx_object = CashTX(
                tx_type='d',
                cash_before=cash_before,
                cash_after=cash_obj.cash,
                amount=cash,
                tx_time=cash_obj.updated,
                user=request.user,
            )
            cashtx_object.save()
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            return render(request, 'error.html', { 'form': form })

@login_required
def withdrawcash(request):
    page_title = 'Form for cash withdrawal'
    cash = float(Cash.objects.get(user=request.user))
    username = request.user
    form = WithdrawCashForm()
    context = {
        'cash': cash,
        'username': username,
        'form': form,
        'action': 'withdraw',
        'resource': 'withdraw-preview',
        'page_title': page_title,
    }
    return render(request, 'cash-action.html', context)


@login_required
def withdrawpreview(request):
    if request.method == 'POST':
        page_title = 'Preview Your Instruction to Withdraw'
        form = WithdrawCashForm(request.POST)
        if form.is_valid():
            context = {
                'form': form,
                'page_title': page_title, 
            }
            return render(request, 'withdraw-preview.html', context)     
        else:
            pass


@login_required
def confirmwithdraw(request):
    if request.method == 'POST':
        form = WithdrawCashForm(request.POST)
        if form.is_valid():
            cash = form.cleaned_data['cash']
            cash_obj = get_object_or_404(Cash, user=request.user)
            if cash_obj.cash < cash:
                context = {
                    'cash': float(Cash.objects.get(user=request.user)),
                    'username': request.user,
                    'form': form,
                    'action': 'withdraw',
                    'resource': 'withdraw-preview',
                    'page_title': 'Error occcured',
                    'error_msg': 'Not enough cash to withdraw, please try again!' 
                }
                return render(request, 'cash-action.html', context)
            cash_before = cash_obj.cash
            cash_obj.cash -= cash
            cash_obj.save()
            cashtx_object = CashTX(
                tx_type='w',
                cash_before=cash_before,
                cash_after=cash_obj.cash,
                amount=cash,
                tx_time=cash_obj.updated,
                user=request.user,
            )
            cashtx_object.save()
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            return render(request, 'error.html', { 'form': form })
