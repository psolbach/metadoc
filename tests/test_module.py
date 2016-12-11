#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import asynctest
import pytest

from asynctest.mock import patch
from metadoc import Metadoc

class MetadocModuleTest(asynctest.TestCase):
  def setUp(self):
    self.url = "https://theintercept.com/2016/11/26/laura-ingraham-lifezette/"
    article_path = "tests/fixtures/theintercept.com/laura-ingraham-lifezette.html"
    with open(article_path, 'r') as article:
      self.article_html=article.read()
    
    self.metadoc = Metadoc(url=self.url, html=self.article_html)
  
  @asynctest.ignore_loop
  def test_init(self):
    assert self.metadoc.url == self.url
    assert self.metadoc.html == self.article_html

  @asynctest.ignore_loop
  def test_query_all(self):
    self.metadoc.query_all()
    result = self.metadoc.return_ball()
    assert result

  @asynctest.ignore_loop
  def test_extract(self):
    self.metadoc.query_extract()
    assert self.metadoc.extractor

  @asynctest.ignore_loop
  async def test_social(self):
    await self.metadoc.query_social()
    assert self.metadoc.activity

  @asynctest.ignore_loop
  async def test_domain(self):
    self.metadoc.query_domain()
    assert self.metadoc.domain

  @asynctest.ignore_loop
  async def test_no_url_fail(self):
    with pytest.raises(AttributeError):
      Metadoc()

  @asynctest.ignore_loop
  async def test_invalid_url_fail(self):
    with pytest.raises(Exception):
      from metadoc import Metadoc
      foo = Metadoc(url="https://theintercept.com/404/", html=None)

  async def test_no_html(self):
    metadoc = Metadoc(url=self.url)
    metadoc.query_all()
