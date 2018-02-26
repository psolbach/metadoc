# -*- coding: utf-8 -*-
import asynctest
from metadoc.install import install_nltk_sets

class MetadocInstallTest(asynctest.TestCase):
  def setUp(self):
    return

  @asynctest.ignore_loop
  def test_install(self):
    install_nltk_sets()
