import os
from dotenv import load_dotenv
from pathlib import Path 

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

WEATHER_APPID = os.getenv('WEATHER_APPID')
CURRENCY_APPID = os.getenv('CURRENCY_APPID')
PORT = os.getenv('PORT')
DEBUG = os.getenv('DEBUG')

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'dw': 'https://rss.dw.com/rdf/rss-en-all',
             'espn': 'http://www.espn.com/espn/rss/news',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'nasa': 'http://www.nasa.gov/rss/dyn/breaking_news.rss',
             'nba': 'http://www.espn.com/espn/rss/nba/news',
             }

DEFAULTS = {'link': 'bbc',
            'city': 'Munich',
            'currency_from': 'EUR',
            'currency_to': 'RSD',
            'currencies': ['AUD', 'CAD', 'CHF', 'EUR', 'RSD', 'SEK', 'USD']}


WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={wx_appid}&units=metric"
CURRENCY_URL = "https://openexchangerates.org//api/latest.json?app_id={curr_appid}"

