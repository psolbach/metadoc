#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__title__ = 'Metadoc - Postmodern news article metadata service'
__copyright__ = 'Copyright 2016, Paul Solbach'
__author__ = 'Paul Solbach'
__license__ = 'MIT'

import concurrent
import json
import bottle
from bottle import response, request, get, route, run, abort, error
from metadoc import Metadoc

bottle.BaseRequest.MEMFILE_MAX = 1024 * 1024 # up max POST payload size to 1MB

@error(404)
def error404(error):
  return json.dumps({'code': 404,'message': 'url param is missing.'})

@get('/social')
def social_article():
  """GET data url required"""
  response.content_type = 'application/json'
  url = request.query.getone("url")
  if not url:
    abort(404)

  metadoc = Metadoc(url=url)
  payload = metadoc.query(mode="social", fmt="social")

  return json.dumps(payload)

@get('/extract')
def extract_article():
  """GET data url required"""
  response.content_type = 'application/json'
  url = request.query.getone("url")
  if not url:
    abort(404)

  metadoc = Metadoc(url=url)
  metadoc._prepare()
  metadoc._query_domain()
  metadoc._query_extract()

  payload = metadoc._render() # Preserve order
  return json.dumps(payload)

@get('/full')
def full_article():
  """GET data url required"""
  response.content_type = 'application/json'
  url = request.query.getone("url")
  if not url:
    abort(404)

  metadoc = Metadoc(url=url)
  payload = metadoc.query()

  return json.dumps(payload)


run(host='localhost', reloader=True, port=6060)
