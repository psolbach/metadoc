#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import asynctest
import datetime
import json
import jmespath
import urllib.parse

from asynctest.mock import patch
from metadoc.social import ActivityCount
from metadoc.social.providers import providers

class MetadocActivityCountTest(asynctest.TestCase):
    def setUp(self):
        self.url = "https://theintercept.com/2016/11/26/laura-ingraham-lifezette/"
        self.activity = ActivityCount(url=self.url)

    @asynctest.ignore_loop
    def test_init(self):
        assert self.activity.url == self.url

    def mocked_get_json(self, url):
        escaped_url = urllib.parse.quote(url, safe='')
        with open("tests/fixtures/activity_endpoints/{0}.json".format(escaped_url), 'r') as file:
          file_content=file.read()

        json_response = json.loads(file_content)
        provider = urllib.parse.urlparse(url).netloc.split(".")[1]
        setattr(self, provider, json_response)

        return file_content

    @patch.object(ActivityCount, 'get_json')
    async def test_get_all_local(self, _mocked_func):
        _mocked_func.side_effect = self.mocked_get_json

        for metrics in self.activity.responses:
          provider_data = [p for p in providers if p["provider"] == metrics["provider"]]
          test_data = getattr(self, metrics["provider"], None)
          test_metric_count = jmespath.search(provider_data[0]["metrics"][0]["path"], test_data)
          returned_metric_count = metrics["metrics"][0]["count"]
          assert test_metric_count == returned_metric_count

    async def test_get_all_remote(self):
        await self.activity.get_all(self.loop)
        assert len(self.activity.responses) > 0

    async def test_invalid_url(self):
        activity = ActivityCount(url="nourlatall")
        res = await activity.collect_sharecount(url="nourlatall", provider="foo")
        assert res == None
