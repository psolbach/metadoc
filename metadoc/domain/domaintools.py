#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import math
import tldextract
from datetime import datetime, timedelta
from .lookup import whois_date_registered
from .check import check_credibility

class Domaintools(object):
  """Gather various metadata like whois informaion
  and blacklist status about any given hostname
  """
  def __init__(self, url=None):
    self.url = url or None
    self.get_domain(url)

  def get_domain(self, url):
    no_fetch_extract = tldextract.TLDExtract(suffix_list_urls=None)
    tld = no_fetch_extract(url)
    self.domain = "{}.{}".format(tld.domain, tld.suffix)

  def get_date_registered(self):
    self.date_registered = whois_date_registered(self.domain)

  def check_credibility(self):
    self.credibility = check_credibility(self.domain)

  def get_all(self):
    if not self.domain: return
    self.get_date_registered()
    self.check_credibility()
    
    if self.date_registered:
      self.recalculate_fake_confidence()
      self.date_registered_iso = self.date_registered.isoformat()

  def recalculate_fake_confidence(self):
    # Adds .2 to fake_confidence if website was registered delta 1y
    one_year_ago = datetime.now() - timedelta(days=1*365)
    if self.date_registered < one_year_ago: return

    confidence = self.credibility.get("fake_confidence", 0)
    self.credibility["fake_confidence"] = float(confidence) + .2

  async def async_get_all(self, loop):
    asyncio.set_event_loop(loop)
    return await loop.run_in_executor(None, self.get_all)
