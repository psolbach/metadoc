#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import asynctest

from asynctest.mock import patch
from metadoc.extract.html import HtmlMeta

def get_html_meta(article_path):
    with open(article_path, 'r') as article:
        html = article.read()
        return HtmlMeta(html)
    return None

class MetadocHtmMetaTest(asynctest.TestCase):

    @asynctest.ignore_loop
    def test_date(self):
        paths = [
            "tests/fixtures/guardian.com/florida-shooting-suspect-charged-questions-nikolas-cruz.html",
            "tests/fixtures/zeit.de/pressefreiheit-tuerkei-inhaftierte-journalisten-deniz-yuecel-freedeniz.html",
            "tests/fixtures/theintercept.com/iphones-secretly-send-call-history-to-apple-security-firm-says.html",
            "tests/fixtures/nytimes/skeleton-ghana-jamaica.html",
            "tests/fixtures/wired.com/inside-the-mind-of-amanda-feilding-countess-of-psychedelic-science.html",
            "tests/fixtures/theverge.com/spacex-falcon-9-launch-starlink-microsat-2a-2b-paz-watch-live.html",
            "tests/fixtures/faz.net/dass-wir-ueberwacht-werden-ist-klar-aber-von-wem-und-wie-eine-spurensuche-15445555.html",
            "tests/fixtures/invalid/invalid.html"
        ]
        objs = [get_html_meta(path) for path in paths]

        # published_data
        assert objs[0].extract_pub_date() == "2018-02-16T00:01:52+00:00"
        assert objs[1].extract_pub_date() == "2018-02-16T10:59:47+00:00"
        assert objs[2].extract_pub_date() == None
        assert objs[3].extract_pub_date() == "2018-02-15T18:44:34+00:00"
        assert objs[4].extract_pub_date() == "2018-02-15T20:40:04+00:00"
        assert objs[5].extract_pub_date() == "2018-02-15T18:54:21+00:00"
        assert objs[6].extract_pub_date() == "2018-02-15T08:22:05+00:00"
        assert objs[7].extract_pub_date() == None

        # modified_date
        assert objs[0].extract_mod_date() == "2018-02-16T09:51:54+00:00"
        assert objs[1].extract_mod_date() == "2018-02-16T10:59:47+00:00"
        assert objs[2].extract_mod_date() == None
        assert objs[3].extract_mod_date() == "2018-02-16T05:45:23+00:00"
        assert objs[4].extract_mod_date() == None
        assert objs[5].extract_mod_date() == None
        assert objs[6].extract_mod_date() == "2018-02-15T09:29:16+00:00"
        assert objs[7].extract_mod_date() == None
