#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__title__ = 'Doxhund - Postmodern news article metadata service'
__copyright__ = 'Copyright 2016, Paul Solbach'
__author__ = 'Paul Solbach'
__license__ = 'MIT'

import asyncio
import concurrent
import requests

from .domain import Domaintools
from .extract import Extractor
from .social import ActivityCount

class Doxhund(object):
  """Doxhund API
  """
  def __init__(self, url=None, html=None, **kwargs):
    """Initialize with
    :param url: The article url we shall investigate, required.
    :param html: You can pass in the article html manually, optional.
    """
    self.html = html
    self.url = url
    
    if not url:
      raise AttributeError('Missing \"url\" attribute.')

  def query_all(self):
    """Combine all available resources"""
    self.extractor = Extractor(self.html) # Named entities, synthetic summaries
    self.activity = ActivityCount(self.url) # Social activity from various networks
    self.domain = Domaintools(self.url) # Domain whois date, blacklisting
    subtasks = []

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    for c in [self.activity, self.extractor, self.domain]:
      subtasks.append(c.async_get_all(loop))

    loop.run_until_complete(asyncio.wait(subtasks, loop=loop))
    loop.close()

  def return_ball(self):
    return self._render()

  def query_domain(self):
    Domaintools(url).get_all()

  def query_social(self):
    ActivityCount(url).get_all()

  def query_ner(self):
    if not self.html: self._request_url()
    Extractor(html).get_all()

  def _render(self):
    """Construct response dict after partial or complete
    queries to various sources
    """
    return {
      "url": self.url,
      "title": getattr(self.extractor, "title", None),
      "authors": getattr(self.extractor, "authors", None),
      "image": getattr(self.extractor, "image", None),
      "social": getattr(self.activity, "responses", None),
      "language": getattr(self.extractor, "language", None),

      "text": {
        "fulltext": getattr(self.extractor, "fulltext", None),
        "pullquotes": getattr(self.extractor, "pullquotes", None),
        "reading_time": getattr(self.extractor, "reading_time", None),
        "contenthash": getattr(self.extractor, "contenthash", None)
      },
      
      "entities": {
        "names": getattr(self.extractor, "entities", None),
        "keywords": getattr(self.extractor, "keywords", None),
      },
      
      "domain": {
        "name": getattr(self.domain, "domain", None),
        "credibility": getattr(self.domain, "credibility", None),
        "date_registered": getattr(self.domain, "date_registered_iso", None),
        "favicon": "https://logo.clearbit.com/{0}?size=200".format(getattr(self.domain, "domain", None)),
      }
    }

  def _request_url(self):
    """In case no html parameter was provided to the constructor"""
    req = requests.get(self.url).content 
    if req.status_code != 200:
      raise Exception('Requesting article body \
        failed with {1} status code.'.format(req.status_code))

    self.html = req.content # after except

