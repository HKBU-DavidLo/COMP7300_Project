import subprocess
from subprocess import Popen, PIPE
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

    r3 = requests.get('https://finnhub.io/api/v1/quote?symbol=' +
                      search+'&token=c0n55kv48v6v1q0c1okg')

    data = r.json()
    news = r2.json()
    price = r3.json()

    try:
        currency = data['currency']
        current_price = str('{:,}'.format(price['c']))
    except:
        currency = "N/A"
        current_price = ""

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
            'marketCapitalization': data['currency']+str('{:,}'.format(data['marketCapitalization']))+' million',
            'shareOutstanding': str('{:,}'.format(data['shareOutstanding']))+' millions of Shares',
            'weburl': data['weburl'],
            'logo': data['logo'],
            'currency': currency,
            'current_price': current_price,
            'final_postings': final_postings,

        }
    else:
        stuff_for_frontend = {'search': search, }

    # models.Search.objects.create(search=search)
    return render(request, 'news/new_search.html', stuff_for_frontend)

<<<<<<< HEAD
=======

def prediction(request):
    try:

        predictstock = request.POST.get('predictstock')
        if predictstock == "":
            predictstock = "AAPL"
            return render(request, 'news/base.html')
        else:
            if request.method == 'POST':
                {'predictstock': predictstock}
                #subprocess.check_call(['python3', './prediction/ai_lstm.py',predictstock])
                process = subprocess.run(['python3', './prediction/ai_lstm.py', predictstock],
                                         check=True, stdout=subprocess.PIPE, universal_newlines=True)
                output = process.stdout
                words = output.split()
                lastpprice = (words[-1])
            # nb lowercase 'python'
                prediction = {'predictstock': predictstock,
                              'lastpprice': lastpprice}
            return render(request, 'news/base.html', prediction)
    except subprocess.CalledProcessError:
        print("empty symbol")
>>>>>>> f73c158588dac4abe8ae3d32670044340c333ade
