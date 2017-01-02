#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from subprocess import call
from setuptools import setup, find_packages
from setuptools.command.install import install as _install

version = '0.3.5'

def _post_install(dir):
  return
  # call([sys.executable, '__install__.py'],
  #   cwd=os.path.join(dir, 'metadoc'))

class CustomInstall(_install):
  """Do stuff after setup."""
  def run(self):
    _install.run(self)
    self.execute(_post_install, (self.install_lib,),
      msg="Running post install task")

setup(
  name='metadoc',
  version=version,
  description="Post-truth era news article metadata service.",
  long_description="",
  classifiers=[ # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    "Programming Language :: Python :: 3.5",
    "Topic :: Internet :: WWW/HTTP", 
    "Development Status :: 3 - Alpha",
    "License :: OSI Approved :: MIT License",
    "Intended Audience :: Developers",
    "Operating System :: POSIX :: Linux",
    "Environment :: Web Environment",
    ], 

  keywords=["scraping", "metadata", "news article"],
  author='Paul Solbach',
  author_email='p@psolbach.com',
  url='https://github.com/psolbach/metadoc',
  license='MIT',
  cmdclass={'install': CustomInstall},
  packages=find_packages(exclude=['tests']),
  include_package_data=True,
  zip_safe=False,
  install_requires=[
    'aiohttp==1.1.5',
    'asynctest==0.9.0',
    'bottle==0.12.10',
    'jmespath==0.9.0',
    'langdetect==1.0.7',
    'libextract==0.0.12',
    'nltk==3.2.1',
    'pytest==3.0.5',
    'pytest-cov==2.4.0',
    'numpy==1.11.2',
    'tldextract==2.0.2',
    'requests==2.12.2',
    'whois==0.7'
  ]
)