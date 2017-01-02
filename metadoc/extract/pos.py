#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Averaged perceptron classifier. Implementation geared for simplicity rather than
efficiency. Adapted from @hankcs, cf. https://github.com/hankcs/AveragedPerceptronPython/blob/master/LICENSE
Based on http://honnibal.wordpress.com/2013/09/11/a-good-part-of-speechpos-tagger-in-about-200-lines-of-python/
"""

from collections import defaultdict
import pickle
import random
import logging
import os

PICKLE = os.path.join(os.path.dirname(__file__), "data/tagger-0.3.5.pickle")
TRAINING_SET = os.path.join(os.path.dirname(__file__), "data/training_set.txt")

logging.basicConfig(level=logging.INFO)

def do_train():
  tagger = AveragedPerceptronTagger(autoload=False)
  logging.info('Reading corpus.')
  training_data = []
  sentence = ([], [])

  for line in open(TRAINING_SET):
    params = line.split(' ')
    if len(params) != 2: continue

    sentence[0].append(params[0])
    sentence[1].append(params[1])

    if params[0] == '.':
      training_data.append(sentence)
      sentence = ([], [])

  logging.info('training corpus size : %d', len(training_data))
  logging.info('Start training...')
  tagger.train(training_data, save_loc=PICKLE)

class AveragedPerceptron(object):
  '''An averaged perceptron, as implemented by Matthew Honnibal.
  '''

  def __init__(self):
    # Each feature gets its own weight vector, so weights is a dict-of-dicts
    self.weights = {}
    self.classes = set()
    # The accumulated values, for the averaging. These will be keyed by
    # feature/clas tuples
    self._totals = defaultdict(int)
    # The last time the feature was changed, for the averaging. Also
    # keyed by feature/clas tuples
    # (tstamps is short for timestamps)
    self._tstamps = defaultdict(int)
    # Number of instances seen
    self.i = 0

  def predict(self, features):
    '''Dot-product the features and current weights and return the best label.'''
    scores = defaultdict(float)
    for feat, value in features.items():
      if feat not in self.weights or value == 0:
        continue
      weights = self.weights[feat]
      for label, weight in weights.items():
        scores[label] += value * weight
    # Do a secondary alphabetic sort, for stability
    return max(self.classes, key=lambda label: (scores[label], label))

  def update(self, truth, guess, features):
    '''Update the feature weights.'''
    def upd_feat(c, f, w, v):
      param = (f, c)
      self._totals[param] += (self.i - self._tstamps[param]) * w
      self._tstamps[param] = self.i
      self.weights[f][c] = w + v

    self.i += 1
    if truth == guess:
      return None
    for f in features:
      weights = self.weights.setdefault(f, {})
      upd_feat(truth, f, weights.get(truth, 0.0), 1.0)
      upd_feat(guess, f, weights.get(guess, 0.0), -1.0)
    return None

  def average_weights(self):
    '''Average weights from all iterations.'''
    for feat, weights in self.weights.items():
      new_feat_weights = {}
      for clas, weight in weights.items():
        param = (feat, clas)
        total = self._totals[param]
        total += (self.i - self._tstamps[param]) * weight
        averaged = round(total / float(self.i), 3)
        if averaged:
          new_feat_weights[clas] = averaged
      self.weights[feat] = new_feat_weights
    return None

  # def save(self, path):
  #   '''Save the pickled model weights.'''
  #   return pickle.dump(dict(self.weights), open(path, 'w'))

  # def load(self, path):
  #   '''Load the pickled model weights.'''
  #   self.weights = pickle.load(open(path))
  #   return None

class AveragedPerceptronTagger(object):
  '''Greedy Averaged Perceptron tagger, as implemented by Matthew Honnibal.
  :param load: Load the pickled model upon instantiation.
  '''

  START = ['-START-', '-START2-']
  END = ['-END-', '-END2-']
  AP_MODEL_LOC = PICKLE

  def __init__(self, autoload=False):
    self.model = AveragedPerceptron()
    self.tagdict = {}
    self.classes = set()

    if autoload:
      self.load(self.AP_MODEL_LOC)

  def tag(self, corpus):
    '''Tags a string `corpus`.'''
    # Assume untokenized corpus has \n between sentences and ' ' between words
    s_split = lambda t: t.split('\n')
    w_split = lambda s: s.split()

    def split_sents(corpus):
      for s in s_split(corpus):
        yield w_split(s)

    prev, prev2 = self.START
    tokens = []

    for words in split_sents(corpus):
      context = self.START + [self._normalize(w) for w in words] + self.END
      for i, word in enumerate(words):
        tag = self.tagdict.get(word)
        if not tag:
          features = self._get_features(i, word, context, prev, prev2)
          tag = self.model.predict(features)

        tokens.append((word, tag.strip()))
        prev2 = prev
        prev = tag

    return tokens

  def named_entities(self, tags):
    '''return sequential named entities,
    IO classification isn't as accurate here, since we're not differentiating between PERSON and ORGANIZATION.
    Still, this is fast and in many cases suited to the task.

    [('The', 'DT'), ('extraordinary', 'JJ'), ('phenomenon', 'NN'), ('of', 'IN'), ('fake', 'JJ'), 
    ('news', 'NN'), ('spread', 'NN'), ('by', 'IN'), ('Facebook', 'NNP'), ('and', ''), ('other', 'JJ'), 
    ('social', 'JJ'), ('media', 'NNS'), ('during', 'IN'), ('the', 'DT'), ('2016', 'CD'), ('presidential', 'JJ'), 
    ('election', 'NN'), ('has', 'VBZ'), ('been', 'VBN'), ('largely', 'RB'), ('portrayed', 'VBN'), ('as', 'IN'), 
    ('a', 'DT'), ('lucky', 'JJ'), ('break', 'NN'), ('for', 'IN'), ('Donald', 'NNP'), ('Trump', 'NNP')]
    '''

    ent, entities = [], []
    tags_len = len(tags)-1
    push_ent = lambda x: entities.append(" ".join(ent))

    for i, tag in enumerate(tags):
      if tag[1] == "NNP":
        ent.append(tag[0])
        if i == tags_len:
          push_ent(ent)

      elif len(ent):
        push_ent(ent)
        ent = []
    
    return entities

  def train(self, sentences, save_loc=None, nr_iter=5):
    '''Train a model from sentences, and save it at ``save_loc``. ``nr_iter``
    controls the number of Perceptron training iterations.
    :param sentences: A list of (words, tags) tuples.
    :param save_loc: If not ``None``, saves a pickled model in this location.
    :param nr_iter: Number of training iterations.
    '''
    self._make_tagdict(sentences)
    self.model.classes = self.classes
    for iter_ in range(nr_iter):
      c = 0
      n = 0
      for words, tags in sentences:
        prev, prev2 = self.START
        context = self.START + [self._normalize(w) for w in words] \
             + self.END
        for i, word in enumerate(words):
          guess = self.tagdict.get(word)
          if not guess:
            feats = self._get_features(i, word, context, prev, prev2)
            guess = self.model.predict(feats)
            self.model.update(tags[i], guess, feats)
          prev2 = prev
          prev = guess
          c += guess == tags[i]
          n += 1
      random.shuffle(sentences)
      logging.info("Iter {0}: {1}/{2}={3}".format(iter_, c, n, _pc(c, n)))
    self.model.average_weights()
    
    # Pickle as a binary file
    if save_loc is not None:
      pickle.dump((self.model.weights, self.tagdict, self.classes),
            open(save_loc, 'wb'), -1)
    
    return None

  def load(self, loc=None):
    '''Load a pickled model.'''
    try:
      w_td_c = pickle.load(open(loc, 'rb'))
    except IOError:
      raise IOError("Invalid perceptrontagger.pickle file.")

    self.model.weights, self.tagdict, self.classes = w_td_c
    self.model.classes = self.classes
    return None

  def _normalize(self, word):
    '''Normalization used in pre-processing.
    - All words are lower cased
    - Digits in the range 1800-2100 are represented as !YEAR;
    - Other digits are represented as !DIGITS
    :rtype: str
    '''
    if '-' in word and word[0] != '-':
      return '!HYPHEN'
    elif word.isdigit() and len(word) == 4:
      return '!YEAR'
    elif word[0].isdigit():
      return '!DIGITS'
    else:
      return word.lower()

  def _get_features(self, i, word, context, prev, prev2):
    '''Map tokens into a feature representation, implemented as a
    {hashable: float} dict. If the features change, a new model must be
    trained.
    '''

    def add(name, *args):
      features[' '.join((name,) + tuple(args))] += 1

    i += len(self.START)
    features = defaultdict(int)
    # It's useful to have a constant feature, which acts sort of like a prior
    add('bias')
    add('i suffix', word[-3:])
    add('i pref1', word[0])
    add('i-1 tag', prev)
    add('i-2 tag', prev2)
    add('i tag+i-2 tag', prev, prev2)
    add('i word', context[i])
    add('i-1 tag+i word', prev, context[i])
    add('i-1 word', context[i - 1])
    add('i-1 suffix', context[i - 1][-3:])
    add('i-2 word', context[i - 2])
    add('i+1 word', context[i + 1])
    add('i+1 suffix', context[i + 1][-3:])
    add('i+2 word', context[i + 2])
    return features

  def _make_tagdict(self, sentences):
    '''Make a tag dictionary for single-tag words.'''
    counts = defaultdict(lambda: defaultdict(int))

    for words, tags in sentences:
      for word, tag in zip(words, tags):
        counts[word][tag] += 1
        self.classes.add(tag)
    freq_thresh = 20
    ambiguity_thresh = 0.97

    for word, tag_freqs in counts.items():
      tag, mode = max(tag_freqs.items(), key=lambda item: item[1])
      n = sum(tag_freqs.values())
      # Don't add rare words to the tag dictionary
      # Only add quite unambiguous words
      if n >= freq_thresh and (float(mode) / n) >= ambiguity_thresh:
        self.tagdict[word] = tag


def _pc(n, d):
  return (float(n) / d) * 100
