#!/usr/local/bin/python3
import settings
import datetime, math, feedparser, requests
from flask import Flask, render_template, request, make_response

# config
WEATHER_URL = settings.WEATHER_URL
CURRENCY_URL = settings.CURRENCY_URL

app = Flask(__name__)

@app.route('/')
def index():
    articles, link = get_feed()
    feeds = sorted(settings.RSS_FEEDS)
    weather = get_weather()
    currency_from, currency_to = get_currencies()
    rate = get_rate(currency_from, currency_to)

    response = make_response(render_template('index.html',
                                             articles=articles,
                                             feeds=feeds,
                                             link=link,
                                             weather=weather,
                                             currency_from=currency_from,
                                             currency_to=currency_to,
                                             rate=rate,
                                             currencies=sorted(settings.DEFAULTS['currencies'])))

    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie("link", link, expires=expires)
    response.set_cookie("city", weather['city'], expires=expires)
    response.set_cookie("currency_from", currency_from, expires=expires)
    response.set_cookie("currency_to", currency_to, expires=expires)
    return response


def get_feed():
    link = get_value_with_defaults('link')
    feed = feedparser.parse(settings.RSS_FEEDS[link])
    return feed['entries'][:10], link


def get_weather():
    city = get_value_with_defaults('city')
    api_url = WEATHER_URL.format(city=city, wx_appid=settings.WEATHER_APPID)
    data = requests.get(api_url).json()
    weather = None
    
    if data.get('message') == 'city not found':
        weather = None
        weather = {'city': 'Not found',
                   'country': '',
                   'description': '',
                   'temperature': 'n/a',
                   'wind': 'n/a'
                   }
    if data.get('weather'):
        weather = {'city': data['name'],
                   'country': data['sys']['country'],
                   'description': data['weather'][0]['description'],
                   'temperature': math.ceil(data['main']['temp']),
                   'wind': "{} km/h".format(math.ceil(data['wind']['speed']))
                   }
    return weather


def get_currencies():
    return get_value_with_defaults('currency_from'), get_value_with_defaults('currency_to')


def get_rate(frm, to):
    all_currency = requests.get(CURRENCY_URL.format(curr_appid=settings.CURRENCY_APPID))
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
    return settings.DEFAULTS[key]

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=settings.PORT, debug=settings.DEBUG)
