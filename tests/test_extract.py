#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import asynctest

from asynctest.mock import patch
from doxhund.extract import Extractor
from doxhund.extract import html

class DoxhundExtractorTest(asynctest.TestCase):
  def setUp(self):
    article_path = "tests/fixtures/theintercept.com/laura-ingraham-lifezette.html"
    with open(article_path, 'r') as article:
      self.article_html=article.read()

    self.extractor = Extractor(self.article_html)

  @asynctest.ignore_loop
  def test_init(self):
    assert self.extractor.html == self.article_html

  async def test_get_all_local(self):
    await self.extractor.async_get_all(self.loop)
    assert self.extractor.contenthash == "61ffed47a1a3e32e29829665ffa1e76e"
    assert self.extractor.title == "Some Fake News Publishers Just Happen to Be Donald Trump’s Cronies"