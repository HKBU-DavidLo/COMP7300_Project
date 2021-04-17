import requests
from django.shortcuts import render
from requests.compat import quote_plus
from . import models
from datetime import datetime, timezone, date, timedelta
import pytz


def home(request):
    return render(request, 'news/base.html')


def new_search(request):
    search = request.POST.get('search')
    if search == "":
        search = "AAPL"
    else:
        search = request.POST.get('search')
    r = requests.get(
        'https://finnhub.io/api/v1/stock/profile2?symbol='+search+'&token=c0n55kv48v6v1q0c1okg')

    today = date.today().strftime("%Y-%m-%d")
    ndays_prior = (datetime.today() - timedelta(days=7)).strftime("%Y-%m-%d")

    r2 = requests.get(
        'https://finnhub.io/api/v1/company-news?symbol='+search+'&from='+ndays_prior+'&to='+today+'&token=c0n55kv48v6v1q0c1okg')

    data = r.json()
    news = r2.json()

    if not(data == {}):
        final_postings = []

        for new in news:
            new_headline = new['headline']
            new_datetime = datetime.fromtimestamp(
                new['datetime'], tz=pytz.timezone('Asia/Hong_Kong'))
            new_image = new['image']
            new_source = new['source']
            new_summary = new['summary']
            new_url = new['url']
            final_postings.append(
                (new_headline, new_datetime, new_image, new_source, new_summary, new_url))

        stuff_for_frontend = {
            'search': search,
            'name': data['name'],
            'exchange': data['exchange'],
            'marketCapitalization': data['currency']+str('{:,}'.format(data['marketCapitalization']))+' Million',
            'shareOutstanding': str('{:,}'.format(data['shareOutstanding']))+' Millions of Shares',
            'weburl': data['weburl'],
            'logo': data['logo'],
            'final_postings': final_postings,
        }
    else:
        stuff_for_frontend = {'search': search, }

    # models.Search.objects.create(search=search)
    return render(request, 'news/new_search.html', stuff_for_frontend)

import subprocess

def prediction(request):
    if request.method == 'POST':
        subprocess.check_call(['python3', './prediction/ai_lstm.py'])  # nb lowercase 'python'
   