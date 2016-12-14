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
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'espn': 'http://www.espn.com/espn/rss/news',
             'nba': 'http://www.espn.com/espn/rss/nba/news',
             'nasa': 'http://www.nasa.gov/rss/dyn/breaking_news.rss'}

DEFAULTS = {'link': 'bbc',
            'city': 'Amsterdam'}

# @app.route('/')
# def index():
#     # get customized headlines based on user input
#     link = urllib.request.args.get('link')
#     if not link:
#         link = DEFAULTS['link']
#     articles = get_feed(link)




@app.route('/')
def get_feed():
    query = request.args.get('link')
    if not query or query.lower() not in RSS_FEEDS:
        link = 'bbc'
    else:
        link = query.lower()

    feed = feedparser.parse(RSS_FEEDS[link])
    return render_template('index.html',
                           articles=feed['entries'][:10],
                           link=link.upper(),
                           feeds=sorted(RSS_FEEDS),
                           weather=get_weather())


def get_weather():
    query = request.args.get('city')
    if not query:
        query = DEFAULTS['city']
    query = query.replace(" ", "")
    api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&APPID=dd99b39031d13629eb69a50e9a4457c7&units=metric" \
        .format(query)
    response = urllib.request.urlopen(api_url).read()
    data = json.loads(response.decode())
    weather = None
    if data.get('weather'):
        weather = {'city': data['name'],
                   'country': data['sys']['country'],
                   'description': data['weather'][0]['description'],
                   'temperature': math.ceil(data['main']['temp']),
                   'wind': "{} km/h".format(math.ceil(data['wind']['speed']))
                   }
    return weather


if __name__ == '__main__':
    app.run(port=5000, debug=True)
