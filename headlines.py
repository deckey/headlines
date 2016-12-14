import json
import math
import urllib

import feedparser
from flask import Flask
from flask import render_template

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'espn': 'http://www.espn.com/espn/rss/news',
             'nba': 'http://www.espn.com/espn/rss/nba/news',
             'nasa': 'http://www.nasa.gov/rss/dyn/breaking_news.rss'}


@app.route('/')
@app.route('/<link>')
def get_feed(link='bbc'):
    if link not in RSS_FEEDS:
        link = 'bbc'
    feed = feedparser.parse(RSS_FEEDS[link])
    weather = get_weather('Amsterdam,NL')
    return render_template('index.html',
                           articles=feed['entries'][:10],
                           link=link.upper(),
                           feeds=sorted(RSS_FEEDS),
                           weather=weather)


def get_weather(query):
    api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&APPID=dd99b39031d13629eb69a50e9a4457c7&units=metric".format(
        query)
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
