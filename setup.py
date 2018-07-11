#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os.path
import sys
import re
from subprocess import call
from setuptools import setup, find_packages
from setuptools.command.install import install as _install
from setuptools.command.sdist import sdist as _sdist
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

with open('./README.md') as f:
    long_description = f.read()

requirements_txt = open("./requirements.txt").read()
main_py = open('metadoc/__init__.py').read()
metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", main_py))


def _post_install():
        from metadoc.install import install_nltk_sets
        install_nltk_sets()

class DevInstall(_install):
    def run(self):
        call(["pip install -r ./requirements-dev.txt --no-clean"], shell=True)
        self.execute(_post_install, (), msg="Installing nltk sets!")
        _install.run(self)

class CustomInstall(_sdist):

    def run(self):
        call(["pip install -r ./requirements.txt --no-clean"], shell=True)
        self.execute(_post_install, (), msg="Installing nltk sets!")
        _sdist.run(self)


class BdistEggInstall(_bdist_wheel):

   def run(self):
        call(["pip install -r ./requirements.txt --no-clean"], shell=True)
        self.execute(_post_install, (), msg="Installing nltk sets!")
        _bdist_wheel.run(self)

setup(
    name='metadoc',
    version=metadata["version"],
    description="Post-truth era news article metadata service.",
    long_description=long_description,
    long_description_content_type='text/markdown',
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
    author=metadata["author"],
    author_email='p@psolbach.com',
    url='https://github.com/praise-internet/metadoc',
    license=metadata["license"],
    cmdclass={'sdist': CustomInstall, 'develop': DevInstall, 'bdist_wheel': BdistEggInstall},
    packages=find_packages(exclude=['tests']),
    install_requires=requirements_txt.strip().split("\n"),
    include_package_data=True,
    zip_safe=False
)
