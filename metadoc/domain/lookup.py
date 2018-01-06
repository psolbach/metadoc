#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib
import whois
import datetime

def whois_date_registered(domain):
  try:
    query = whois.query(domain) # silently fails in corporate env, vocally fails behind proxy
  except Exception as e:
    query = None
    pass

  # if query.creation_date == "before aug-1996": query.creation_date = datetime.datetime(1996) # .co.uk edge case
  # elif type(query.creation_date) is not "date": query = None
  return query.creation_date if query else None