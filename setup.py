#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os.path
import sys
from subprocess import call
from setuptools import setup, find_packages
from setuptools.command.install import install as _install


version_file = open('VERSION')
version = version_file.read().strip()

def _post_install():
        from metadoc.install import install_nltk_sets
        install_nltk_sets()

class CustomInstall(_install):
    def run(self):
        call(["pip install -r requirements.txt --no-clean"], shell=True)
        self.execute(_post_install, (), msg="Installing nltk sets!")
        _install.run(self)

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
    cmdclass={'install': CustomInstall, 'develop': CustomInstall},
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False
)
