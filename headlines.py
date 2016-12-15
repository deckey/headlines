#!/usr/local/bin/python3
import json
import math
import urllib

import feedparser
import urllib.request
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'espn': 'http://www.espn.com/espn/rss/news',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'nasa': 'http://www.nasa.gov/rss/dyn/breaking_news.rss',
             'nba': 'http://www.espn.com/espn/rss/nba/news'}

DEFAULTS = {'link': 'bbc',
            'city': 'Amsterdam',
            'currency_from': 'EUR',
            'currency_to': 'RSD',
            'currencies': ['AUD', 'CAD', 'CHF', 'EUR', 'RSD', 'SEK']}

WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&APPID=dd99b39031d13629eb69a50e9a4457c7&units=metric"
CURRENCY_URL = "https://openexchangerates.org//api/latest.json?app_id=445bea4da73a4b828cdd0166859dfda7"


@app.route('/')
def index():
    return render_template('index.html',
                           articles=get_feed(),
                           feeds=sorted(RSS_FEEDS),
                           weather=get_weather(),
                           currency_from=get_currencies()[0],
                           currency_to=get_currencies()[1],
                           rate=get_rates(*get_currencies()),
                           currencies=sorted(DEFAULTS['currencies']))


def get_feed():
    query = request.args.get('link')
    if not query or query.lower() not in RSS_FEEDS:
        link = DEFAULTS['link']
    else:
        link = query.lower()

    feed = feedparser.parse(RSS_FEEDS[link])
    return feed['entries'][:10]


def get_weather():
    query = request.args.get('city')
    if not query:
        query = DEFAULTS['city']
    query = query.replace(" ", "")
    api_url = WEATHER_URL.format(query)
    response = urllib.request.urlopen(api_url).read().decode()
    data = json.loads(response)
    weather = None
    if data.get('weather'):
        weather = {'city': data['name'],
                   'country': data['sys']['country'],
                   'description': data['weather'][0]['description'],
                   'temperature': math.ceil(data['main']['temp']),
                   'wind': "{} km/h".format(math.ceil(data['wind']['speed']))
                   }
    return weather


def get_currencies():
    currency_from = request.args.get('currency_from')
    if not currency_from:
        currency_from = DEFAULTS['currency_from']
    currency_to = request.args.get('currency_to')
    if not currency_to:
        currency_to = DEFAULTS['currency_to']
    return currency_from, currency_to


def get_rates(frm, to):
    all_currency = urllib.request.urlopen(CURRENCY_URL).read().decode()
    parsed = json.loads(all_currency)
    frm_rate = parsed.get('rates')[frm.upper()]
    to_rate = parsed.get('rates')[to.upper()]
    rate = round(to_rate / frm_rate, 4)
    return rate


if __name__ == '__main__':
    app.run(port=5000, debug=True)
