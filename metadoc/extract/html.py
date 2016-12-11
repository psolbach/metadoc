#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import lxml.etree, lxml.html
from collections import ChainMap

class HtmlMeta(object):
  """Extract metadata from html.
  Needs work, e.g. handling multiple @property=author tags,
  detect if author content is a social media destination.
  """
  def __init__(self, html, encoding="UTF-8"):
    self.html = html or None
    self.parser = lxml.html.HTMLParser(encoding=encoding)
    self.document = lxml.html.fromstring(html, parser=self.parser)
    self._jsonld_xpath = lxml.etree.XPath('descendant-or-self::script[@type="application/ld+json"]')
    self._metatag_xpath = lxml.etree.XPath("//meta")

  def _extract_items(self, get_item, xpath):
    items = [item for item in map(get_item, xpath(self.document)) if item]
    return dict(ChainMap(*items))

  def _get_metatag_item(self, node):
    name = node.xpath('@property' or '@itemprop' or '@name')
    content = node.xpath('@content')

    return {name[0]: content[0]} \
      if (name and content) else None

  def _get_jsonld_item(self, node):
    return json.loads(node.xpath('string()'))

  def extract_title(self):
    title = self.document.xpath("(//title)[1]//text()")
    return title[0] if len(title) else None

  def extract(self):
    self.metatags = self._extract_items(self._get_metatag_item, self._metatag_xpath)
    self.jsonld = self._extract_items(self._get_jsonld_item, self._jsonld_xpath)
    self.title = self.extract_title()
    return