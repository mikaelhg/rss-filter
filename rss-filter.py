#!/usr/bin/python2
# -*- coding: utf-8 -*-

from flask import *
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
from werkzeug.contrib.atom import AtomFeed
import feedparser
from time import mktime
from datetime import datetime
import requests

from webapp import scrape, model

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@app.route('/amppar-it.atom')
def ampparit():
    data = feedparser.parse('http://feeds.feedburner.com/ampparit-it')
    feed = AtomFeed(data.feed.title,
                    feed_url=request.url, url=request.url_root)
    for d in data.entries:
        category_ok = 'it' in [x['term'] for x in d.tags]
        author_ok = d.author not in model.BANNED_AUTHORS
        if category_ok and author_ok:
            r1 = requests.get(d.link, allow_redirects=False)
            actual_url = r1.headers['location']
            content_type, content = scrape.scrape(actual_url)
            feed.add(d.title, id=actual_url, link=actual_url,
                     content_type=content_type, content=content,
                     author=d.author, updated=datetime.fromtimestamp(mktime(d.updated_parsed)))
    return feed

if __name__ == "__main__":
    manager.run()
