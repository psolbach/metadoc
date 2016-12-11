#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib
import whois

def whois_date_registered(domain):
  query = whois.query(domain) # silently fails in corporate env, vocally fails behind proxy
  return query.creation_date if query else None