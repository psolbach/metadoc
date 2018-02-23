#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import glob
import nltk
import os
import time

def remove_zips(data_dir):
     glob_path = os.path.join(data_dir, '**/*.zip')
     for filename in glob.iglob(glob_path, recursive=True):
         print("Removing {}...".format(filename))
         os.remove(filename)

def install_nltk_sets():
    DATA_DIR = os.path.join(os.path.dirname(__file__), "extract/data")
    REQUIRED_CORPORA = [
        'brown', # Required for FastNPExtractor
        'punkt', # Required for WordTokenizer
        'wordnet', # Required for lemmatization and Wordnet
        'maxent_ne_chunker',
        'stopwords',
        'words'
    ]

    for each in REQUIRED_CORPORA:
        print(('[+] Downloading corpus:  "{0}"'.format(each)))
        nltk.download(each, download_dir=DATA_DIR)

    from metadoc.extract.pos import do_train
    print('[+] Training tagger now.')
    do_train()
    remove_zips(DATA_DIR)
    return

if __name__ == "__main__":
    install_nltk_sets()
