#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import asynctest
import pytest

from asynctest.mock import patch
from doxhund import Doxhund

class DoxhundModuleTest(asynctest.TestCase):
  def setUp(self):
    self.url = "https://theintercept.com/2016/11/26/laura-ingraham-lifezette/"
    article_path = "tests/fixtures/theintercept.com/laura-ingraham-lifezette.html"
    with open(article_path, 'r') as article:
      self.article_html=article.read()
    
    self.doxhund = Doxhund(url=self.url, html=self.article_html)
  
  @asynctest.ignore_loop
  def test_init(self):
    assert self.doxhund.url == self.url
    assert self.doxhund.html == self.article_html

  @asynctest.ignore_loop
  def test_query_all(self):
    self.doxhund.query_all()
    result = self.doxhund.return_ball()
    assert result

  @asynctest.ignore_loop
  def test_extract(self):
    self.doxhund.query_extract()
    assert self.doxhund.extractor

  @asynctest.ignore_loop
  async def test_social(self):
    await self.doxhund.query_social()
    assert self.doxhund.activity

  @asynctest.ignore_loop
  async def test_domain(self):
    self.doxhund.query_domain()
    assert self.doxhund.domain

  @asynctest.ignore_loop
  async def test_no_url_fail(self):
    with pytest.raises(AttributeError):
      Doxhund()

  @asynctest.ignore_loop
  async def test_invalid_url_fail(self):
    with pytest.raises(Exception):
      from doxhund import Doxhund
      foo = Doxhund(url="https://theintercept.com/404/", html=None)

  async def test_no_html(self):
    assert Doxhund(url=self.url).html is not None
