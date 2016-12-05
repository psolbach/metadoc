#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: 
# - twine to publish!

from setuptools import setup, find_packages
version = '0.2.16'

setup(
  name='docshund',
  version=version,
  description="Postmodern news article metadata extraction.",
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
  maintainer='Paul Solbach',
  maintainer_email='p@psolbach.com',
  url='https://github.com/psolbach/docshund',
  license='MIT',

  packages=find_packages(exclude=['tests']),
  include_package_data=True,
  zip_safe=False,
  install_requires=[]
)