#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from metadoc import Metadoc

if __name__ == '__main__':
  url = "https://theintercept.com/2016/11/17/iphones-secretly-send-call-history-to-apple-security-firm-says/"
  metadoc = Metadoc(url=url)
  metadoc.query_social()

  print(metadoc.activity.responses)
