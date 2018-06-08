# -*- coding: utf-8 -*-
import asynctest
import pytest
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
    result = self.metadoc.query()
    assert result

  @asynctest.ignore_loop
  def test_extract(self):
    self.metadoc.query("extract")
    assert self.metadoc.extractor

  @asynctest.ignore_loop
  def test_social(self):
    self.metadoc.query("social")
    assert self.metadoc.activity

  @asynctest.ignore_loop
  def test_social_return(self):
    result = self.metadoc.query("social", "social")
    assert list(result.keys()) == ["url", "social", "__version__"]

  @asynctest.ignore_loop
  def test_domain(self):
    self.metadoc.query("domain")
    assert self.metadoc.domain

  @asynctest.ignore_loop
  def test_no_url_fail(self):
    with pytest.raises(AttributeError):
      Metadoc()

  @asynctest.ignore_loop
  def test_invalid_url_fail(self):
      metadoc = Metadoc(url="https://theintercept.com/404/", html=None)
      result = metadoc.query()
      assert result["errors"][0] ==  "Requesting article body failed with 404 status code."

  @asynctest.ignore_loop
  def test_no_html(self):
    metadoc = Metadoc(url=self.url)
    metadoc.query()

  @asynctest.ignore_loop
  def test_check_result(self):
      self.metadoc._check_result({})

  @asynctest.ignore_loop
  def test_invalid_charset_check(self):
      s = "Von da an beginnt fÃ¤r die meisten jedoch der hektische Teil."
      assert self.metadoc._check_invalid_encoding(s) == True
      s = "Von da an beginnt fÃ¼r die meisten jedoch der hektische Teil."
      assert self.metadoc._check_invalid_encoding(s) == True
      s = "Von da an beginnt fÃ¶r die meisten jedoch der hektische Teil."
      assert self.metadoc._check_invalid_encoding(s) == True
      s = "Von da an beginnt fÃ¼r die meisten jedoch der hektische Teil."
      assert self.metadoc._check_invalid_encoding(s) == True

      s = "DE PÃŠRA"
      assert self.metadoc._check_invalid_encoding(s) == False

  @asynctest.ignore_loop
  def test_invalid_t3n(self):
      metadoc = Metadoc(url="https://t3n.de/news/remote-work-home-office-heimarbeit-erfahrungsbericht-1018248/", html=None)
      result = metadoc.query()
      assert result["title"] ==  "Remote Workers Life: „Das Home-Office löst viele Probleme, schafft aber auch neue“"
