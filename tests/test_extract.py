# -*- coding: utf-8 -*-
import unittest
from unittest.mock import patch
from metadoc.extract import Extractor
from metadoc.extract.pos import do_train

class MetadocExtractorTest(unittest.TestCase):
  def setUp(self):
    article_path = "tests/fixtures/theintercept.com/laura-ingraham-lifezette.html"
    with open(article_path, 'r') as article:
      self.article_html=article.read()

    self.extractor = Extractor(self.article_html)

  def test_init(self):
    assert self.extractor.html == self.article_html

  def test_without_ft(self):
    self.extractor.fulltext = ""
    self.extractor.detect_language()
    assert self.extractor

  def test_get_all_local(self):
    do_train()
    self.extractor.get_all()
    assert self.extractor.contenthash == "2b374ca41d42bd582e500e6cdbc936ef"
    assert self.extractor.title == "Some Fake News Publishers Just Happen to Be Donald Trump’s Cronies"
