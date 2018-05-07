# -*- coding: utf-8 -*-
import asyncio
import jmespath
import json
import logging
import requests
import signal
import time

from aiohttp import ClientSession
from .providers import providers

logger = logging.getLogger(__name__)

class ActivityCount(object):
    """Gather activity/share stats from social APIs"""

    def __init__(self, url=None):
        self.url = url or None
        self.responses = []

    def get_all(self, loop):
        activity_tasks = []
        for provider in providers:
            url = provider["endpoint"].format(self.url)
            task = asyncio.ensure_future(self.collect_sharecount(url, provider))
            activity_tasks.append(task)

        return asyncio.gather(*activity_tasks)

    async def get_json(self, url):
        async with ClientSession() as session:
            async with session.get(url) as response:
                return await response.read()

    async def collect_sharecount(self, url, provider):
        try:
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
        except Exception as exc:
            logger.error("Collecting sharecount failed!")
            logger.exception(exc)

