#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import difflib
import operator
import nltk
import numpy
import string
import re

from nltk.tokenize import RegexpTokenizer
from .pos import AveragedPerceptronTagger

tokenizer = RegexpTokenizer(r'\w+')

def isPunct(word):
  pattern = r"(`|\.|#|\$|%|&|\'|\(|\)|\*|\||\+|,|-|—|/|:|;|<|=|>|\?|@|\[|\]|\^|_|`|{|}|~|”|“|’)"
  return re.search(pattern, word) is not None

class EntityExtractor(object):
  def __init__(self, text):
    self.perceptron_tagger = AveragedPerceptronTagger(autoload=True)
    self.stopwords = set(nltk.corpus.stopwords.words())
    self.top_fraction = 70 # consider top candidate keywords only
    self.sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    self.sentences = self.sent_detector.tokenize(text)

  def _calculate_word_scores(self, word_list):
    """Quick and dirty, inspired by Sujit Pal's RAKE implementation.
    """
    word_freq = nltk.FreqDist()
    for word in word_list:
      word_freq[word] += 1
    
    word_scores = {k:v for k, v in word_freq.items() if v > 0}
    return word_scores

  # def _get_mt_median(self, word_scores):
  #   median = numpy.median([v for k, v in word_scores.items()])
  #   return {k: v for k, v in word_scores.items() if v > median}

  def _filter_distance(self, words):
    close_matches = []
    wordlist = set(words[:]) # deepcopy

    for word in words:
      if word in close_matches: continue
      matches = difflib.get_close_matches(word, wordlist, 2)
      if len(matches) > 1:
        close_matches += matches[1:]

    return wordlist.difference(close_matches)

  def _sort_and_filter(self, word_scores):
    n_words = len(word_scores)
    sorted_word_scores = sorted(word_scores.items(), key=operator.itemgetter(1), reverse=True)
    top_words = sorted_word_scores[0:int(n_words/100*self.top_fraction)]
    punct_filtered = [k[0] for k in top_words if not isPunct(k[0])]
    distance_filtered = self._filter_distance(punct_filtered)
    return list(distance_filtered)

  def _contains_stopword(self, ent):
    filtered = [word.lower() in self.stopwords for word in ent.split(" ")]
    return True in filtered

  def get_scored_entities(self):
    named_ents = []

    for sent in self.sentences:
      pos_tags = self.perceptron_tagger.tag(" ".join(nltk.word_tokenize(sent)))
      entities = self.perceptron_tagger.named_entities(pos_tags)
      named_ents += [ent for ent in entities if not self._contains_stopword(ent)]

    ent_scores = self._calculate_word_scores(named_ents)
    self.ent_scores = ent_scores
    return ent_scores

  def get_names(self):
    filtered_names = {k: v for k, v in self.ent_scores.items() if len(k.split(" ")) > 1}
    top_names = self._sort_and_filter(filtered_names)
    return top_names[:8]
    
  def get_keywords(self):
    filtered_keywords = {k.lower(): v for k, v in self.ent_scores.items() if len(k.split(" ")) == 1}
    top_keywords = self._sort_and_filter(filtered_keywords)
    return top_keywords[:8]
