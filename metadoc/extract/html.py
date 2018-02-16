#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import lxml.etree, lxml.html
from dateutil.parser import parse
from dateutil.tz import tzoffset
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
        self._links_xpath = lxml.etree.XPath("//link")

        self.links = None
        self.jsonld = None
        self.links = None

    def _extract_items(self, get_item, xpath):
        items = [item for item in map(get_item, xpath(self.document)) if item]
        return dict(ChainMap(*items))

    def _get_metatag_item(self, node):
        name = node.xpath('@property') or node.xpath('@itemprop') or node.xpath('@name')
        content = node.xpath('@content')

        return {name[0]: content[0]} \
          if (name and content) else None

    def _get_link_item(self, node):
        name = node.xpath('@rel')
        content = node.xpath('@href')

        return {name[0]: content[0]} \
          if (name and content) else None

    def _get_jsonld_item(self, node):
        return json.loads(node.xpath('string()'))

    def extract_title(self):
        title = self.document.xpath("(//title)[1]//text()")
        return title[0] if len(title) else None

    def _query_date(self, xpath_rules):
        for xpath_rule in xpath_rules:
            dates = self.document.xpath(xpath_rule)
            if len(dates) > 0:
                try:
                    date = parse(dates[0].get("content"))
                    return date.astimezone().astimezone(
                                tzoffset(None, 0)).replace(microsecond=0).isoformat()
                except:
                    pass
        return None

    def extract_pub_date(self):
        xpaths = [
            "//meta[@name='date']",
            "//meta[@property='article:published_time']",
            "//meta[@property='article:published']",
            "//meta[@name='parsely-pub-date']",
            "//meta[@name='DC.date.issued']",
        ]
        return self._query_date(xpaths)

    def extract_mod_date(self):
        xpaths = [
            "//meta[@property='article:modified_time']",
            "//meta[@property='article:modified']",
            "//meta[@name='last-modified']",
        ]
        return self._query_date(xpaths)

    def extract(self):
        self.metatags = self._extract_items(self._get_metatag_item, self._metatag_xpath)
        self.jsonld = self._extract_items(self._get_jsonld_item, self._jsonld_xpath)
        self.links = self._extract_items(self._get_link_item, self._links_xpath)
        self.title = self.extract_title()
        self.published_date = self.extract_pub_date()
        self.modified_date = self.extract_mod_date()
        return
