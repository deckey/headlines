#!/usr/local/bin/python3
import datetime
import math

import feedparser
import requests
from flask import Flask, render_template, request, make_response

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
            'currencies': ['AUD', 'CAD', 'CHF', 'EUR', 'RSD', 'SEK', 'USD']}

WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&APPID=dd99b39031d13629eb69a50e9a4457c7&units=metric"
CURRENCY_URL = "https://openexchangerates.org//api/latest.json?app_id=445bea4da73a4b828cdd0166859dfda7"


@app.route('/')
def index():
    articles, link = get_feed()
    feeds = sorted(RSS_FEEDS)
    weather = get_weather()
    currency_from, currency_to = get_currencies()
    rate = get_rate(*get_currencies())

    response = make_response(render_template('index.html',
                                             articles=articles,
                                             feeds=feeds,
                                             link=link,
                                             weather=weather,
                                             currency_from=currency_from,
                                             currency_to=currency_to,
                                             rate=rate,
                                             currencies=sorted(DEFAULTS['currencies'])))

    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie("link", link, expires=expires)
    response.set_cookie("city", weather['city'], expires=expires)
    response.set_cookie("currency_from", currency_from, expires=expires)
    response.set_cookie("currency_to", currency_to, expires=expires)
    return response


def get_feed():
    link = get_value_with_defaults('link')
    feed = feedparser.parse(RSS_FEEDS[link])
    return feed['entries'][:10], link


def get_weather():
    city = get_value_with_defaults('city')
    city = city.replace(" ", "")
    api_url = WEATHER_URL.format(city)
    response = requests.get(api_url)
    data = response.json()
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
    currency_from = get_value_with_defaults('currency_from')
    currency_to = get_value_with_defaults('currency_to')
    return currency_from, currency_to


def get_rate(frm, to):
    all_currency = requests.get(CURRENCY_URL)
    parsed = all_currency.json()
    frm_rate = parsed.get('rates')[frm.upper()]
    to_rate = parsed.get('rates')[to.upper()]
    rate = round(to_rate / frm_rate, 4)
    return rate


def get_value_with_defaults(key):
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULTS[key]


if __name__ == '__main__':
    app.run(port=5000, debug=True)
