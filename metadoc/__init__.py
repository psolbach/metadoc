#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__title__ = 'Metadoc - Postmodern news article metadata service'
__copyright__ = 'Copyright 2016, Paul Solbach'
__author__ = 'Paul Solbach'
__license__ = 'MIT'
__version__ = '0.7.0'

import asyncio
import time
import concurrent
import requests
import urllib.parse

from .domain import Domaintools
from .extract import Extractor
from .social import ActivityCount

import logging
logging.basicConfig(level=logging.DEBUG)

class Metadoc(object):
  def __init__(self, url=None, html=None, **kwargs):
    """Metadoc API, initialize with
    :param url: The article url we shall investigate, required.
    :param html: You can pass in the article html manually, optional.
    """

    self.html = html or None
    self.url = url or None

    if not url:
      raise AttributeError('Missing \"url\" attribute.')

    if not self.html:
      self._request_url()

    self.extractor = Extractor(html=self.html) # Named entities, synthetic summaries
    self.activity = ActivityCount(url=self.url) # Social activity from various networks
    self.domain = Domaintools(url=self.url) # Domain whois date, blacklisting

  def query_all(self):
    """Combine all available resources"""
    subtasks = []
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
    subtasks.append(loop.run_in_executor(executor, self.extractor.get_all))
    subtasks.append(loop.run_in_executor(executor, self.domain.get_all))
    subtasks.append(self.activity.get_all(loop))

    loop.run_until_complete(asyncio.wait(subtasks, loop=loop))
    loop.close()

  def return_ball(self):
    return self._render()

  def return_social(self):
    return {
      "url": self.url,
      "social": getattr(self.activity, "responses", None),
      "__version__": __version__
    }

  def query_domain(self):
    self.domain.get_all()

  def query_social(self):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(self.activity.get_all(loop))
    loop.close()

  def query_extract(self):
    self.extractor.get_all()

  def _render(self):
    """Construct response dict after partial or complete
    queries to various sources
    """
    return {
      "url": self.url,
      "title": getattr(self.extractor, "title", None),
      "authors": getattr(self.extractor, "authors", None),
      "canonical_url": getattr(self.extractor, "canonical_url", None),
      "image": getattr(self.extractor, "image", None),
      "social": getattr(self.activity, "responses", None),
      "language": getattr(self.extractor, "language", None),
      "published_date": getattr(self.extractor, "published_date", None),
      "modified_date": getattr(self.extractor, "modified_date", None),
      "scraped_date": getattr(self.extractor, "scraped_date", None),
      "text": {
        "fulltext": getattr(self.extractor, "fulltext", None),
        "summary": getattr(self.extractor, "description", "No summary found."),
        "reading_time": getattr(self.extractor, "reading_time", None),
        "contenthash": getattr(self.extractor, "contenthash", None)
      },

      "entities": {
        "names": getattr(self.extractor, "names", None),
        "keywords": getattr(self.extractor, "keywords", None),
      },

      "domain": {
        "name": getattr(self.domain, "domain", None),
        "credibility": getattr(self.domain, "credibility", None),
        "date_registered": getattr(self.domain, "date_registered_iso", None),
        "favicon": "https://logo.clearbit.com/{0}?size=200".format(getattr(self.domain, "domain", None)),
      },

      "__version__": __version__
    }

  def _request_url(self):
    """In case no html parameter was provided to the constructor"""

    p = urllib.parse.urlparse(self.url)
    netloc = p.netloc or p.path
    path = p.path if p.netloc else ''
    # if not netloc.startswith('www.'):
    #     netloc = 'www.' + netloc

    p = urllib.parse.ParseResult(p.scheme, netloc, path, *p[3:])
    url = p.geturl()

    req = requests.get(url, headers={
      'Accept-Encoding': 'identity, gzip, deflate, *',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    })

    if req.status_code != 200:
      raise Exception('Requesting article body failed with {} status code.'.format(req.status_code))

    self.html = req.text # after except
