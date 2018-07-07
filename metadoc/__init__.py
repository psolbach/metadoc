# -*- coding: utf-8 -*-

__title__ = 'Metadoc - Postmodern news article metadata service'
__copyright__ = 'Copyright 2016, Paul Solbach'
__author__ = 'Paul Solbach'
__license__ = 'MIT'
__version__ = '0.9.0'

import asyncio
import time
import concurrent
import requests
import urllib.parse
import os
import re
import sys
import logging

from .domain import Domaintools
from .extract import Extractor
from .social import ActivityCount

logger = logging.getLogger()
logger.setLevel(os.environ.get("LOGLEVEL", "INFO"))
formatter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s %(message)s')

if not os.environ.get("LAMBDA_TASK_ROOT", False):
    # add stream handler, except for AWS Lambda
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

class Metadoc(object):

    def __init__(self, url=None, html=None, **kwargs):
        """Metadoc API, initialize with
        :param url: The article url we shall investigate, required.
        :param html: You can pass in the article html manually, optional.
        """
        logger.info("Processing url: {}".format(url))

        self.errors = []
        self.html = html or None
        self.url = url or None

        if not self.url:
          raise AttributeError('Missing \"url\" attribute.')

        self.extractor = None
        self.activity = None
        self.domain = None

    def _prepare(self):
        if not self.html:
            self.html = self._request_url()
        self.extractor = Extractor(html=self.html) # Named entities, synthetic summaries
        self.activity = ActivityCount(url=self.url) # Social activity from various networks
        self.domain = Domaintools(url=self.url) # Domain whois date, blacklisting

    def query(self, mode=None, fmt=None):
        data = None
        try:
            self._prepare()
            calls = {
                "social": self._query_social,
                "domain": self._query_domain,
                "extract": self._query_extract,
            }
            calls.get(mode, self._query_all)()
            data = self._render_social() if fmt == "social" else self._render()
            if mode is None:
                self._check_result(data)
        except Exception as exc:
            logger.error("Error when processing {}".format(self.url))
            logger.exception(exc)
            self.errors.append(str(exc))

        # return data or error
        if data is None or self.errors:
            return self._render_errors()
        return data

    def _query_all(self):
        """Combine all available resources"""
        subtasks = []
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
        subtasks.append(loop.run_in_executor(executor, self.extractor.get_all))
        subtasks.append(loop.run_in_executor(executor, self.domain.get_all))
        subtasks.append(self.activity.get_all(loop))

        loop.run_until_complete(asyncio.wait(subtasks, loop=loop))
        loop.close()

    def _query_domain(self):
        self.domain.get_all()

    def _query_social(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(self.activity.get_all(loop))
        loop.close()

    def _query_extract(self):
        self.extractor.get_all()

    def _render_errors(self):
        return {
            "errors": self.errors
        }

    def _render_social(self):
        return {
          "url": self.url,
          "social": getattr(self.activity, "responses", None),
          "__version__": __version__
        }

    def _render(self):
        """Construct response dict after partial or complete
        queries to various sources
        """
        return {
          "url": self.url,
          "title": getattr(self.extractor, "title", None),
          "authors": getattr(self.extractor, "authors", None),
          "canonical_url": getattr(self.extractor, "canonical_url", None),
          "image": getattr(self.extractor, "image", None),
          "social": getattr(self.activity, "responses", None),
          "language": getattr(self.extractor, "language", None),
          "published_date": getattr(self.extractor, "published_date", None),
          "modified_date": getattr(self.extractor, "modified_date", None),
          "scraped_date": getattr(self.extractor, "scraped_date", None),
          "text": {
            "fulltext": getattr(self.extractor, "fulltext", None),
            "summary": getattr(self.extractor, "description", "No summary found."),
            "reading_time": getattr(self.extractor, "reading_time", None),
            "contenthash": getattr(self.extractor, "contenthash", None)
          },
          "entities": {
            "names": getattr(self.extractor, "names", None),
            "keywords": getattr(self.extractor, "keywords", None),
          },
          "domain": {
            "name": getattr(self.domain, "domain", None),
            "credibility": getattr(self.domain, "credibility", None),
            "date_registered": getattr(self.domain, "date_registered_iso", None),
            "favicon": "https://logo.clearbit.com/{0}?size=200".format(getattr(self.domain, "domain", None)),
          },
          "__version__": __version__
        }

    def _check_result(self, res):
        if not res.get("title"):
            logger.warning("No title: {}".format(self.url))
        if not res.get("canonical_url"):
            logger.warning("No canonical url: {}".format(self.url))
        if len(res.get("text", {}).get("fulltext", [])) < 50:
            logger.warning("No or little text: {}".format(self.url))
        if not res.get("entities", {}).get("names"):
            logger.warning("No names: {}".format(self.url))
        if not res.get("entities", {}).get("keywords"):
            logger.warning("No keywords: {}".format(self.url))
        if not res.get("domain", {}).get("name"):
            logger.warning("No domain name: {}".format(self.url))

    def _request_url(self):
        """In case no html parameter was provided to the constructor"""

        p = urllib.parse.urlparse(self.url)
        netloc = p.netloc or p.path
        path = p.path if p.netloc else ''
        # if not netloc.startswith('www.'):
        #     netloc = 'www.' + netloc

        p = urllib.parse.ParseResult(p.scheme, netloc, path, *p[3:])
        url = p.geturl()

        req = requests.get(url, headers={
          'Accept-Encoding': 'identity, gzip, deflate, *',
          'User-Agent': 'Facebot/1.0'
        })

        if req.status_code != 200:
          raise Exception('Requesting article body failed with {} status code.'.format(req.status_code))

        if self._check_invalid_encoding(req.text):
            # check for encoding conflicts (e.g. t3n.de)
            enc_apparent = req.apparent_encoding.lower()
            if req.encoding.lower() != enc_apparent and \
               enc_apparent != "windows-1254":
                logger.info("Switching html encoding: {} -> {}".format(req.encoding, enc_apparent))
                req.encoding = enc_apparent
        return req.text

    def _check_invalid_encoding(self, html):
        r=r'(Ã¼|Ã¤|Ã¶|Ã¼)'
        return True if re.search(r, html, re.I|re.M) else False
