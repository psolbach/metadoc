#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import asynctest
import pytest

class MetadocInstallTest(asynctest.TestCase):
  def setUp(self):
    return

  @asynctest.ignore_loop
  def test_install(self):
    from metadoc.__install__ import install
    assert True