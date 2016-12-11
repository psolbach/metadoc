#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import aiohttp
import asyncio
import jmespath
import json
import logging
import requests
import signal

from .providers import providers

logging.basicConfig(level=logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)

class ActivityCount(object):
  """Gather activity/share stats from social APIs"""
  def __init__(self, url=None):
    self.url = url or None
    self.responses = []

  def establish_client(self, loop):
    self.loop = asyncio.new_event_loop()
    self.client = aiohttp.ClientSession(loop=self.loop)
    asyncio.set_event_loop(self.loop)

  async def async_get_all(self, loop):
    self.establish_client(loop)
    
    for provider in providers:
      url = provider["endpoint"].format(self.url)
      asyncio.ensure_future(self.collect_sharecount(url, provider), loop=self.loop)

    # loop over all providers
    pending = asyncio.Task.all_tasks(loop=self.loop)
    self.loop.run_until_complete(asyncio.gather(*pending, loop=self.loop))
    self.client.close()
    self.loop.close()

  async def get_json(self, url):
    async with self.client.get(url) as response:
      assert response.status == 200
      logging.debug("Got response for URL {0} with statuscode {1}".format(url, response.status))
      response = await response.read()
      return response.decode('utf-8')

  async def collect_sharecount(self, url, provider):
    response = await self.get_json(url)
    j = json.loads(response)

    data = {
      "provider": provider["provider"],
      "metrics": []
    }

    for m in provider["metrics"]:
      data["metrics"].append({
        "count": jmespath.search(m["path"], j),
        "label": m["label"]
      })
    
    self.responses.append(data)
