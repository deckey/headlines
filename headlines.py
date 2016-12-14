import feedparser
from flask import Flask
from flask import render_template

app = Flask(__name__)

BBC_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'espn': 'http://www.espn.com/espn/rss/news',
             'nba': 'http://www.espn.com/espn/rss/nba/news',
             'nasa': 'http://www.nasa.gov/rss/dyn/breaking_news.rss'}


@app.route('/')
@app.route('/<link>')
def get_feed(link='bbc'):
    feed = feedparser.parse(BBC_FEEDS[link])
    return render_template('index.html',
                           articles=feed['entries'][:10],
                           link=link.upper())


if __name__ == '__main__':
    app.run(port=5000, debug=True)
