# Metadoc
[![Build Status](https://travis-ci.org/psolbach/metadoc.svg?branch=master)](https://travis-ci.org/psolbach/metadoc)
[![Coverage Status](https://coveralls.io/repos/github/psolbach/metadoc/badge.svg?branch=master)](https://coveralls.io/github/psolbach/metadoc?branch=master)

Metadoc is a post-truth era news article metadata retrieval service. It does social media activity lookup, source authenticity rating, checksum creation, json-ld and metatag parsing as well as information extraction for named entities, pullquotes, fulltext and other useful things based off of arbitrary article URLs. Also, Metadoc is built to be relatively fast.

## Example

You just throw it any news article URL, and Metadoc will yield.
```python
from metadoc import Metadoc
url = "https://theintercept.com/2016/11/17/iphones-secretly-send-call-history-to-apple-security-firm-says"
metadoc = Metadoc(url=url)
res = metadoc.query()
```
=>
```python
{'__version__': '0.9.0',
 'authors': ['Kim Zetter'],
 'canonical_url': 'https://theintercept.com/2016/11/17/iphones-secretly-send-call-history-to-apple-security-firm-says/',
 'domain': {'credibility': {'fake_confidence': '0.00', 'is_blacklisted': False},
            'date_registered': None,
            'favicon': 'https://logo.clearbit.com/theintercept.com?size=200',
            'name': 'theintercept.com'},
 'entities': {'keywords': ['cellebrite',
                           'fbi',
                           'skype',
                           'intercept',
                           'israeli',
                           'russian',
                           'elcomsoft',
                           'katalov'],
              'names': ['San Bernardino',
                        'Apple CallKit',
                        'Civil Liberties Union',
                        'Phone Breaker',
                        'Apple ID',
                        'Vladimir Katalov',
                        'Financial Times',
                        'Chris Soghoian']},
 'image': 'https://theintercept.imgix.net/wp-uploads/sites/1/2016/11/GettyImages-578052668-s.jpg?auto=compress%2Cformat&q=90&fit=crop&w=1200&h=800',
 'language': 'en',
 'modified_date': None,
 'published_date': '2016-11-17T11:00:36+00:00',
 'scraped_date': '2018-07-10T12:13:46+00:00',
 'social': [{'metrics': [{'count': 7340, 'label': 'sharecount'}],
             'provider': 'facebook'},
            {'metrics': [{'count': None, 'label': 'upvotes'},
                         {'count': None, 'label': 'num_reports'}],
             'provider': 'reddit'},
            {'metrics': [{'count': 0, 'label': 'sharecount'}],
             'provider': 'linkedin'}],
 'text': {'contenthash': '940a62c70db255b4aec378529ae7a2c8',
          'fulltext': 'a guardian of user privacy this year after fighting FBI '
                      'demands to help crack into San Bernardino shooter Syed [...]',
          'reading_time': 439,
          'summary': 'Your call logs get sent to Apple’s servers whenever '
                     'iCloud is on — something Apple does not disclose.'},
 'title': 'iPhones Secretly Send Call\xa0History to Apple, Security Firm Says',
 'url': 'https://theintercept.com/2016/11/17/iphones-secretly-send-call-history-to-apple-security-firm-says'
}
```

## Trustworthiness Check
Metadoc does a basic background check on article sources. This means a simple blacklist-lookup via `whois` data on the domain. Blacklists taken into account include the controversial [PropOrNot](http://www.propornot.com/p/the-list.html). Thus, only if a domain is found on every blacklist do we spit out a `fake_confidence` of 1. The resulting metadata should be taken with a grain of salt.

## Part-of-speech tagging
For speed and simplicity, we decided against `nltk` and instead rely on the Averaged Perceptron as imagined by Matthew Honnibal [@explosion](https://github.com/explosion). The pip install comes pre-trained with a [CoNLL 2000](http://www.cnts.ua.ac.be/conll2000/) training set which works reasonably well to detect proper nouns. Since training is non-deterministic, unwanted stopwords might slip through. If you want to try out other datasets, simply replace `metadoc/extract/data/training_set.txt` with your own and run `metadoc.extract.pos.do_train`.

## Purpose
This library is used in the context of a news-related software undertaking called [Praise](https://praise.press). We're building the first social network dedicated to quality journalism recommendations. Synthesizing what we dub "audience-evaluated content" with automated metadata. If you're intrigued and might want to work with us, feel free to drop a line to [a@praise.press](a@praise.press).   

## Install
Requires python 3.5.

#### Using pip
```shell
pip install metadoc
```

## Develop

#### Mac OS
```shell
brew install python3 libxml2 libxslt libtiff libjpeg webp little-cms2
```
#### Ubuntu
```shell
apt-get install -y python3 libxml2-dev libxslt-dev libtiff-dev libjpeg-dev webp whois
```
#### Fedora/Redhat
```shell
dnf install libxml2-devel libxslt-devel libtiff-devel libjpeg-devel libjpeg-turbo-devel libwebp whois
```
#### Then
```shell
pip3 install -r requirements-dev.txt
python serve.py => serving @ 6060
```

## Test
```shell
py.test -v tests
```
If you happen to run into an error with OSX 10.11 concerning a lazy bound library in PIL,   
just remove `/PIL/.dylibs/liblzma.5.dylib`.

## Todo
* Page concatenation is needed in order to properly calculate wordcount and reading time.
* Authenticity heuristic with sharecount deviance detection (requires state).
* ~~Perf: Worst offender is nltk's pos tagger. Roll own w/ Average Perceptron.~~
* ~~Newspaper's summarize produces pullquotes, fulltext takes a while. Move to libextract?~~

## Contributors
[Martin Borho](https://github.com/mborho)
[Paul Solbach](https://github.com/___paul)

---

Meteadoc is a software product of Praise Internet UG, Hamburg.
Metadoc stems from a pedigree of nice libraries like [goose3](https://github.com/goose3/goose3/tree/master/goose3), [langdetect](https://github.com/Mimino666/langdetect) and [nltk](https://github.com/nltk/nltk).
Metadoc leans on [this](https://github.com/hankcs/AveragedPerceptronPython) perceptron implementation inspired by Matthew Honnibal.    
Metadoc is a work-in-progress.
