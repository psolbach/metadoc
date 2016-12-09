#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import asyncio
import lxml
import nltk
import math
import hashlib

from langdetect import detect
from newspaper.nlp import summarize, keywords
from newspaper.extractors import ContentExtractor
from newspaper.configuration import Configuration
from newspaper import fulltext

from .html import HtmlMeta

class Extractor(object):
  """Entity recognition, pullquote extraction etc.
  """
  def __init__(self, html=None, title=" ", **kwargs):
    self.html = html or None
    self.title = title or None
    self.entities = []

  def detect_language(self):
    """Langdetect is non-deterministic, so to achieve a higher probability
    we attempt detection multiple times and only report success if we get identical results.
    """
    nondet_attempts = [detect(self.fulltext) for i in range(0,2)]
    is_unique = len(set(nondet_attempts)) == 1
    self.language = nondet_attempts[0] if is_unique else False

  def sanitize_html(self):
    # Lxml bails out on html w/ emojis
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
      "]+", flags=re.UNICODE)
  
    self.html = emoji_pattern.sub(r'', self.html)

  def extract_entities(self):
    """Rudimentary NER, label PERSON is unreliable but ok, 
    improve accuracy by combining with other methods.
    Will not work with Python 3.5.2 oddly enough. Investigate.
    """
    for sent in nltk.sent_tokenize(self.fulltext):
      for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
        if hasattr(chunk, 'label') and chunk.label() == 'PERSON' and len(chunk.leaves()) > 1:
          clean_chunk = ' '.join(c[0] for c in chunk.leaves())
          self.entities.append(clean_chunk)

  def extract_text(self):
    """Parse fulltext, do keyword extraction using the newspaper lib
    => newspaper.readthedocs.io
    """
    self.fulltext = fulltext(self.html) # heads up: contains newlines
    self.pullquotes = summarize(title=" ", text=self.fulltext) # array of sentences, unusable as summary
    self.keywords = {k: v for k, v in keywords(self.fulltext).items() if v > 1.015} # filter confidence

  def extract_metadata(self):
    """Sniff for essential and additional metadata via
    either metatags and or json-ld"""
    html_meta = HtmlMeta(self.html)
    html_meta.extract()

    self.authors = html_meta.jsonld.get("authors") \
      or html_meta.metatags.get("article:author") \
      or html_meta.metatags.get("author")

    self.title = html_meta.jsonld.get("headline") or html_meta.title
    self.image = html_meta.metatags.get("twitter:image") or html_meta.jsonld.get("thumbnailUrl")

  def get_contenthash(self):
    """Generate md5 hash over title and body copy in order to keep track
    of changes made to a text, do diffs if necessary
    """
    contentstring = (self.title + self.fulltext).encode("utf-8")
    self.contenthash = hashlib.md5(contentstring).hexdigest()
    return self.contenthash

  def get_reading_time(self):
    """Calculate average reading time in seconds"""
    if not self.fulltext: return None
    wordcount = len(self.fulltext.split())
    self.reading_time = math.floor(wordcount / 300 * 60)

  def get_all(self):
    self.sanitize_html()
    self.extract_text()
    self.extract_entities()
    self.extract_metadata()
    self.detect_language()
    self.get_contenthash()
    self.get_reading_time()
    return

  async def async_get_all(self, loop):
    asyncio.set_event_loop(loop)
    return await loop.run_in_executor(None, self.get_all)
