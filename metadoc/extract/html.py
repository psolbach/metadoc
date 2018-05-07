#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import logging
import lxml.etree, lxml.html
from datetime import datetime
from dateutil.parser import parse
from dateutil.tz import tzoffset
from collections import ChainMap

logger = logging.getLogger(__name__)

class HtmlMeta(object):
    """Extract metadata from html.
    Needs work, e.g. handling multiple @property=author tags,
    detect if author content is a social media destination.
    """
    def __init__(self, html, encoding="UTF-8", tree=None):
        self.html = html or None
        if tree is not None:
            # reuse tree already parsed
            self.document = tree
        else:
            self.parser = lxml.html.HTMLParser(encoding=encoding)
            self.document = lxml.html.fromstring(html, parser=self.parser)
        self._jsonld_xpath = lxml.etree.XPath('descendant-or-self::script[@type="application/ld+json"]')
        self._metatag_xpath = lxml.etree.XPath("//meta")
        self._links_xpath = lxml.etree.XPath("//link")

        self.links = {}
        self.jsonld = {}
        self.metatags = {}

    @property
    def title(self):
        return self.jsonld.get("headline") \
            or self.metatags.get("og:title") \
                or self.extract_title()

    @property
    def description(self):
        return self.metatags.get("og:description") \
            or self.metatags.get("description", "").strip()

    @property
    def canonical_url(self):
        return self.links.get("canonical")

    @property
    def image(self):
        return self.metatags.get("og:image") \
            or self.jsonld.get("thumbnailUrl")

    def _extract_ld_authors(self):
        # extract from jsonld
        ld_authors = self.jsonld.get("author", {})
        # sanitize ld structure
        if type(ld_authors) == str:
            ld_authors = {"name": ld_authors}
        ld_authors = [a["name"] for a in ld_authors] if type(ld_authors) == list else ld_authors.get("name", False)
        return ld_authors

    @property
    def authors(self):
        # get a value from trove
        authors = self._extract_ld_authors() \
            or self.metatags.get("author") \
                or self.metatags.get("article:author") \
                    or self.metatags.get("dcterms.creator") \
                        or self.metatags.get("article:authorName") \
                            or self.metatags.get("citation_author") \
                                or self.jsonld.get("authors") # intercept

        if authors:
            # ensure list
            if type(authors) != list:
                authors = [authors]
            # strip links
            authors = [a for a in authors if a.startswith("http") == False]

        if not authors:
            # washingtonpost
            xauthors = self.document.xpath("(//span[@itemprop='author'])[1]//span[@itemprop='name']/text()")
            if xauthors:
                authors = xauthors

        return authors if authors else []

    @property
    def published_date(self):
        res = None
        xpaths = [
            "//meta[@name='date']/@content",
            "//meta[@property='article:published_time']/@content",
            "//meta[@property='article:published']/@content",
            "//meta[@name='parsely-pub-date']/@content",
            "//meta[@name='DC.date.issued']/@content",
            "//time[@itemprop='datePublished']/@datetime",
        ]
        res = self._query_date(xpaths)
        if res is None:
            ld_date = self.jsonld.get("datePublished") or self.jsonld.get("dateCreated")
            if ld_date:
                res = self._format_date(ld_date)
        return res

    @property
    def modified_date(self):
        res = None
        xpaths = [
            "//meta[@property='article:modified_time']/@content",
            "//meta[@property='article:modified']/@content",
            "//meta[@name='last-modified']/@content",
        ]
        res = self._query_date(xpaths)
        if res is None:
            ld_date = self.jsonld.get("dateModified")
            if ld_date:
                res = self._format_date(ld_date)
        return res

    @property
    def scraped_date(self):
        return self._format_date(datetime.now())

    def extract(self):
        self.metatags = self._extract_items(self._get_metatag_item, self._metatag_xpath)
        self.jsonld = self._extract_items(self._get_jsonld_item, self._jsonld_xpath)
        self.links = self._extract_items(self._get_link_item, self._links_xpath)

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
        ld = None
        try:
            ld_text = node.text.strip()
            # sanitize if neccessary
            if ld_text.find("<![CDATA[") > -1:
                ld_text = ld_text[ld_text.find("{"):ld_text.rfind("}")+1]

            ld = json.loads(ld_text)
            if type(ld) is list:
                for item in[i for i in ld if i.get("@type") == "NewsArticle"]:
                    return item
        except Exception as exc:
            logger.error("JSON-LD parsing failed")
            logger.exception(exc)
        return ld if ld else {}

    def extract_title(self):
        title = self.document.xpath("(//title)[1]//text()")
        return title[0] if len(title) else None

    def _format_date(self, date_in):
        date = parse(date_in) if type(date_in) is str else date_in
        return date.astimezone().astimezone(
                    tzoffset(None, 0)).replace(microsecond=0).isoformat()

    def _query_date(self, xpath_rules):
        for xpath_rule in xpath_rules:
            dates = self.document.xpath(xpath_rule)
            if len(dates) > 0:
                try:
                    return self._format_date(str(dates[0]))#.get("content"))
                except:
                    pass
        return None
