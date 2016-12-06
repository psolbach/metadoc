#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import asynctest
import datetime
from unittest.mock import patch
from doxhund.domain import Domaintools

class DoxhundDomaintoolsTest(asynctest.TestCase):

  def setUp(self):
    article_path = "tests/fixtures/theintercept.com/laura-ingraham-lifezette.html"
    self.title = "Some Fake News Publishers Just Happen to Be Donald Trump’s Cronies"
    self.url = "https://theintercept.com/2016/11/26/laura-ingraham-lifezette/"
    self.date_registered = datetime.datetime(2009, 10, 1, 0, 0)
    self.domaintools = Domaintools(self.url)

    with open(article_path, 'r') as article:
      self.article_html=article.read()
  
  @asynctest.ignore_loop
  def test_init(self):
    assert self.domaintools.url == self.url
    assert self.domaintools.domain == "theintercept.com"

  @asynctest.ignore_loop
  @patch('doxhund.domain.lookup.get_date_registered')
  async def test_get_all(self, mock_date_registered):
    mock_date_registered.return_value = asynctest.MagicMock(self.date_registered)
    
    loop = asyncio.get_event_loop()
    await self.domaintools.async_get_all(loop)

    credibility_resp = {
      "is_blacklisted": False,
      "fake_confidence": "0.00"
    }

    assert self.domaintools.credibility == credibility_resp
    assert self.domaintools.date_registered == self.date_registered

  @asynctest.ignore_loop
  def test_new_domain(self):
    today = datetime.datetime.now()
    self.domaintools.date_registered = today
    self.domaintools.check_credibility()
    self.domaintools.recalculate_fake_confidence()

    assert self.domaintools.credibility["fake_confidence"] == 0.2

