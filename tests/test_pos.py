#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import asynctest

from asynctest.mock import patch
from metadoc.extract.pos import do_train, AveragedPerceptronTagger

class MetadocPerceptronTest(asynctest.TestCase):
  def setUp(self):
    do_train()

  @asynctest.ignore_loop
  def test_init(self):
    self.perceptron_tagger = AveragedPerceptronTagger(autoload=True)
    tags = self.perceptron_tagger.tag("Rami Eid is studying at Stony Brook University in NY")
    assert len(tags) == 10

