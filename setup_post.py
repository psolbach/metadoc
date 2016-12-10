#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nltk

REQUIRED_CORPORA = [
  'brown', # Required for FastNPExtractor
  'punkt', # Required for WordTokenizer
  'maxent_treebank_pos_tagger',  # Required for NLTKTagger
  'movie_reviews', # Required for NaiveBayesAnalyzer
  'wordnet', # Required for lemmatization and Wordnet
  'averaged_perceptron_tagger',
  'maxent_ne_chunker',
  'stopwords',
  'words' 
]

for each in REQUIRED_CORPORA:
  print(('Downloading "{0}"'.format(each)))
  nltk.download(each)