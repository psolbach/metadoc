#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import itertools
from .blacklists import blacklists

def check_credibility(url):
  plain_lists = [l for l in list(blacklists.values())]
  consolidated_list = list(itertools.chain.from_iterable(plain_lists))
  confidence = consolidated_list.count(url) / len(blacklists)
  unique_set = set(consolidated_list)
  
  return {
    "is_blacklisted": url in consolidated_list,
    "fake_confidence": "{0:.2f}".format(confidence)
  }