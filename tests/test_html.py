#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import asynctest

from asynctest.mock import patch
from metadoc.extract.html import HtmlMeta

def get_html_meta(article_path):
    with open(article_path, 'r') as article:
        html = article.read()
        meta = HtmlMeta(html)
        meta.extract()
        return meta
    return None

class MetadocHtmMetaTest(asynctest.TestCase):

    @asynctest.ignore_loop
    def test_extract(self):
        paths = [
            "guardian.com/florida-shooting-suspect-charged-questions-nikolas-cruz.html",
            "zeit.de/pressefreiheit-tuerkei-inhaftierte-journalisten-deniz-yuecel-freedeniz.html",
            "theintercept.com/iphones-secretly-send-call-history-to-apple-security-firm-says.html",
            "nytimes/skeleton-ghana-jamaica.html",
            "wired.com/inside-the-mind-of-amanda-feilding-countess-of-psychedelic-science.html",
            "theverge.com/spacex-falcon-9-launch-starlink-microsat-2a-2b-paz-watch-live.html",
            "faz.net/dass-wir-ueberwacht-werden-ist-klar-aber-von-wem-und-wie-eine-spurensuche-15445555.html",
            "time.com/jared-kushner-security-clearance-trump-kelly.html",
            "netzpolitik.org/index.html",
            "invalid/invalid.html",
            "bloomberg.com/brexit-talks-in-peril-as-may-rejects-eu-draft-as-unacceptable",
            "buzzfeed.com/so-viel-dreck",
            "bostonreview.net/thad-williamson-almost-inevitable-failure-justice",
            "washingtonpost.com/i-need-loyalty-james-comeys-riveting-prepared-testimony-about-what-trump-asked-him-annotated.html",
            "washingtonpost.com/trump-to-nominate-carson-to-lead-u-s-housing-urban-policy.html",
            "bellingcat.com/six-months-medical-facilities-still-fire.html",
        ]
        objs = [get_html_meta("tests/fixtures/"+path) for path in paths]

        # published_data
        assert objs[0].published_date == "2018-02-16T00:01:52+00:00"
        assert objs[1].published_date == "2018-02-16T10:59:47+00:00"
        assert objs[2].published_date == "2016-11-17T11:00:36+00:00"
        assert objs[3].published_date == "2018-02-15T18:44:34+00:00"
        assert objs[4].published_date == "2018-02-15T20:40:04+00:00"
        assert objs[5].published_date == "2018-02-15T18:54:21+00:00"
        assert objs[6].published_date == "2018-02-15T08:22:05+00:00"
        assert objs[7].published_date == "2018-02-28T03:11:27+00:00"
        assert objs[8].published_date == "2018-02-16T13:46:24+00:00"
        assert objs[9].published_date == None

        # modified_date
        assert objs[0].modified_date == "2018-02-16T09:51:54+00:00"
        assert objs[1].modified_date == "2018-02-16T10:59:47+00:00"
        assert objs[2].modified_date == None
        assert objs[3].modified_date == "2018-02-16T05:45:23+00:00"
        assert objs[4].modified_date == "2018-02-15T20:40:03+00:00"
        assert objs[5].modified_date == "2018-02-15T18:54:21+00:00"
        assert objs[6].modified_date == "2018-02-15T09:29:16+00:00"
        assert objs[7].modified_date == "2018-02-28T15:45:06+00:00"
        assert objs[8].modified_date == "2018-02-16T17:16:57+00:00"
        assert objs[9].modified_date == None

        # title
        assert objs[4].title == "Inside the Mind of Amanda Feilding, Countess of Psychedelic Science"
        assert objs[8].title == "Bundeswehr bereitet sich auf den Kampf gegen Killer-Roboter vor"
        assert objs[9].title == None

        # authors
        assert objs[2].authors == "Kim Zetter"
        assert objs[3].authors == "Randal C. Archibold"
        assert objs[5].authors == "Loren Grush"
        assert objs[8].authors == "Alexander Fanta"
        assert objs[9].authors == None
        assert objs[10].authors == ["Tim Ross", "Ian Wishart"]
        assert objs[11].authors == "Becky Barnicoat"
        assert objs[12].authors == "Thad Williamson"
        assert objs[13].authors == ["Amber Phillips", "Peter W. Stevenson"]
        assert objs[14].authors == "Elise Viebeck"
        assert objs[15].authors == None # link stripped

        # summary
        assert objs[8].description.startswith("Wissenschafter und Aktivisten warnen seit") == True
        assert objs[9].description == ""

        # canonical url
        assert objs[4].canonical_url == "https://www.wired.com/story/inside-the-mind-of-amanda-feilding-countess-of-psychedelic-science/"
        assert objs[9].canonical_url == None

        # images
        assert objs[6].image == "http://media2.faz.net/ppmedia/1912312546/1.5445566/article_multimedia_overview/scoring-teaser.png"
        assert objs[9].image== None

        """for x, obj in enumerate(objs):
            #print(x, obj.jsonld)
            print(x, obj.canonical_url)
            print(x, obj.image)"""


