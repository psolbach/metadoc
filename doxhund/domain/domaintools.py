#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import tldextract
from datetime import datetime, timedelta
from .lookup import get_registered_date
from .check import check_credibility

class Domaintools(object):
  """Gather various metadata like whois informaion
  and blacklist status about any given hostname
  """
  def __init__(self, url):
    self.url = url
    self.get_domain(url)

  def get_domain(self, url):
    tld = tldextract.extract(url)
    self.domain = "{}.{}".format(tld.domain, tld.suffix)

  def get_all(self):
    if not self.domain: return
    self.date_registered = get_registered_date(self.domain)
    self.credibility = check_credibility(self.domain)
    
    if self.date_registered:
      self.recalculate_fake_confidence()
      self.date_registered_iso = self.date_registered.isoformat()
    
    return

  def recalculate_fake_confidence(self):
    # Adds .2 to fake_confidence if website was registered delta 1y
    one_year_ago = datetime.now() - timedelta(days=1*365)
    if self.date_registered < one_year_ago: return

    confidence = self.credibility.get("fake_confidence", 0)
    self.credibility["fake_confidence"] = math.floor(float(confidence) + .2)

  async def async_get_all(self, loop):
    asyncio.set_event_loop(loop)
    return await loop.run_in_executor(None, self.get_all)
