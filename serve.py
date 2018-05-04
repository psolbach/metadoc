#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__title__ = 'Metadoc - Postmodern news article metadata service'
__copyright__ = 'Copyright 2016, Paul Solbach'
__author__ = 'Paul Solbach'
__license__ = 'MIT'

import concurrent
import json
import bottle
from bottle import response, request, post, route, run, abort, error
from metadoc import Metadoc

bottle.BaseRequest.MEMFILE_MAX = 1024 * 1024 # up max POST payload size to 1MB

@error(404)
def error404(error):
  return json.dumps({'code': 404,'message': 'Params html or title missing.'})

@post('/social')
def social_article():
  """POST data url required, html optional"""
  response.content_type = 'application/json'
  url = request.forms.get("url")

  if not url:
    abort(404)

  metadoc = Metadoc(url=url)
  payload = metadoc.query(mode="social", fmt="social")

  return json.dumps(payload)

@post('/extract')
def extract_article():
  """POST data url required, html optional"""
  response.content_type = 'application/json'
  url = request.forms.get("url")

  if not url:
    abort(404)

  metadoc = Metadoc(url=url)
  metadoc._query_domain()
  metadoc._query_extract()

  payload = metadoc._render() # Preserve order
  return json.dumps(payload)

@post('/full')
def full_article():
  """POST data url required, html optional"""
  response.content_type = 'application/json'
  url, html = request.forms.get("url"), request.forms.get("html")

  if not url:
    abort(404)

  metadoc = Metadoc(url=url, html=html)
  payload = metadoc.query_all()

  return json.dumps(payload)


run(host='localhost', reloader=True, port=6060)
