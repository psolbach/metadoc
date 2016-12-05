#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__title__ = 'Docshund - Postmodern news article metadata service'
__copyright__ = 'Copyright 2016, Paul Solbach'
__author__ = 'Paul Solbach'
__license__ = 'MIT'

import concurrent
import json
import bottle
from bottle import response, request, post, route, run, abort, error
from docshund import Docshund

bottle.BaseRequest.MEMFILE_MAX = 1024 * 1024 # up max POST payload size to 1MB

@error(404)
def error404(error):
  return json.dumps({'code': 404,'message': 'Params html or title missing.'})

@post('/article')
def article():
  """POST data url required, html optional"""
  response.content_type = 'application/json'
  url, html = request.forms.get("url"), request.forms.get("html")
  
  if not url:
      abort(404)

  docshund = Docshund(url=url, html=html)
  docshund.query_all()

  payload = docshund.return_ball() # Preserve order
  return json.dumps(payload)


run(host='localhost', reloader=True, port=6060)
