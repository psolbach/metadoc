#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import operator
import nltk
import string
from nltk.tokenize import RegexpTokenizer
from nltk.tag.perceptron import PerceptronTagger

tokenizer = RegexpTokenizer(r'\w+')
tagger = PerceptronTagger()

def isPunct(word):
  return len(word) == 1 and word in string.punctuation

def isNumeric(word):
  try:
    float(word) if '.' in word else int(word)
    return True
  except ValueError:
    return False

def isUnwantedTag(word):
  s = nltk.word_tokenize(word)
  tag = tagger.tag(s)[0][1]
  return tag in ['VBD','VBG']

class EntityExtractor(object):
  """Quick and dirty, inspired by Sujit Pal's RAKE implementation.
  Ported to Python3. Additional person/org extraction is unreliable but ok,
  improve accuracy by combining with other methods.
  """
  def __init__(self, text):
    self.stopwords = set(nltk.corpus.stopwords.words())
    self.top_fraction = 85 # consider top candidate keywords only
    self.sentences = nltk.sent_tokenize(text)

  def _generate_candidate_keywords(self, sentences):
    phrase_list = []

    for sentence in sentences:
      words = map(lambda x: "|" if x in self.stopwords else x, tokenizer.tokenize(sentence.lower()))
      phrase = []

      for word in words:
        if word == "|" or isPunct(word):
          if len(phrase) > 0:
            phrase_list.append(phrase)
            phrase = []
        else:
          phrase.append(word)

    return phrase_list

  def _calculate_word_scores(self, phrase_list):
    word_freq = nltk.FreqDist()
    word_degree = nltk.FreqDist()
    
    for phrase in phrase_list:
      degree = len(list((x for x in phrase if not isNumeric(x)))) -1

      for word in phrase:
        word_freq[word] += 1
        word_degree[word] += degree # other words

    for word in word_freq.keys():
      word_degree[word] = word_degree[word] + word_freq[word] # itself
    
    avg_degree = sum(word_degree.values()) / len(word_degree)
    word_scores = {k:v for k, v in word_degree.items() if (v > 0 and not isUnwantedTag(k))}
    return word_scores
    
  def get_keywords(self):
    phrase_list = self._generate_candidate_keywords(self.sentences)
    word_scores = self._calculate_word_scores(phrase_list)
    sorted_word_scores = sorted(word_scores.items(), key=operator.itemgetter(1), reverse=True)
    n_words = len(sorted_word_scores)
    
    top_words = sorted_word_scores[0:int(n_words/self.top_fraction)]
    return {a: b for a, b in top_words}

  def get_names(self):
    entities = []

    for sent in self.sentences:
      pos_tags = tagger.tag(nltk.word_tokenize(sent))
      chunks = nltk.ne_chunk(pos_tags)

      for chunk in chunks:
        if hasattr(chunk, 'label') and chunk.label() == 'PERSON' and len(chunk.leaves()) > 1:
          clean_chunk = ' '.join(c[0] for c in chunk.leaves())
          entities.append(clean_chunk)

    return entities
