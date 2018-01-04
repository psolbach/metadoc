#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib
import whois
import datetime

def whois_date_registered(domain):
  query = whois.query(domain) # silently fails in corporate env, vocally fails behind proxy
  # if query.creation_date == "before aug-1996": query.creation_date = datetime.datetime(1996) # .co.uk edge case
  # elif type(query.creation_date) is not "date": query = None
  return query.creation_date if query else None