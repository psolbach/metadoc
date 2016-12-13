#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import asynctest
import pytest

from asynctest.mock import patch
from metadoc.extract.pos import do_train, AveragedPerceptronTagger

class MetadocPerceptronTest(asynctest.TestCase):
  def setUp(self):
    return

  @asynctest.ignore_loop
  def test_init(self):
    self.perceptron_tagger = AveragedPerceptronTagger(autoload=True)
    tags = self.perceptron_tagger.tag("Rami Eid is studying at Stony Brook University in NY")
    assert len(tags) == 10

  @asynctest.ignore_loop
  def test_string_ends_with_nnp(self):
    self.perceptron_tagger = AveragedPerceptronTagger(autoload=True)
    test_sentence = "The extraordinary phenomenon of fake news spread by Facebook and other \
      social media during the 2016 presidential election has been largely portrayed as a lucky break for Donald Trump"

    tags = self.perceptron_tagger.tag(test_sentence)
    entities = self.perceptron_tagger.named_entities(tags)
    
    assert tags[len(tags)-1][1] == "NNP"
    assert "Donald Trump" in entities

  @asynctest.ignore_loop
  @patch('metadoc.extract.pos.pickle.load')
  def test_no_pickle_found(self, _mocked_func):
    _mocked_func.side_effect = IOError('foo')
    with pytest.raises(IOError):
      AveragedPerceptronTagger(autoload=True)
