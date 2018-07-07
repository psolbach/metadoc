#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os.path
import sys
import re
from subprocess import call
from setuptools import setup, find_packages
from setuptools.command.install import install as _install


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

class CustomInstall(_install):
    def run(self):
        call(["pip install -r ./requirements.txt --no-clean"], shell=True)
        self.execute(_post_install, (), msg="Installing nltk sets!")
        _install.run(self)

setup(
    name='metadoc',
    version=metadata["version"],
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
    author=metadata["author"],
    author_email='p@psolbach.com',
    url='https://github.com/psolbach/metadoc',
    license=metadata["license"],
    cmdclass={'install': CustomInstall, 'develop': DevInstall, 'bdist_wheel': CustomInstall},
    packages=find_packages(exclude=['tests']),
    install_requires=requirements_txt.strip().split("\n"),
    include_package_data=True,
    zip_safe=False
)
