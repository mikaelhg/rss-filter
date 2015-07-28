#!/usr/bin/python2
# -*- coding: utf-8 -*-
import lxml

import requests
from lxml.cssselect import CSSSelector
import lxml.html
import lxml.etree

__MATO78_SELECTOR = CSSSelector('article.status-publish > div > div.bb_padding > p')

def _scrape_mato(url):
    try:
        r = requests.get(url)
        h = lxml.html.fromstring(r.text)
        return 'text', "\n".join([x.text_content() for x in __MATO78_SELECTOR(h)])
    except lxml.etree.ParseError, requests.exceptions.HTTPError:
        return 'text', ''

_URLS = {
    'http://www.mato78.com/': _scrape_mato
}

def scrape(url):
    for k, v in _URLS.iteritems():
        if url.startswith(k):
            return v(url)
    return 'text', ''

