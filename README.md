# Metadoc
[![Build Status](https://travis-ci.org/psolbach/metadoc.svg?branch=master)](https://travis-ci.org/psolbach/metadoc)
[![Coverage Status](https://coveralls.io/repos/github/psolbach/metadoc/badge.svg?branch=master)](https://coveralls.io/github/psolbach/metadoc?branch=master)

Metadoc is a post-truth era news article metadata retrieval service and API mashup. It does social media activity lookup, source authenticity rating, checksum creation, json-ld and metatag parsing as well as information extraction for named entities, pullquotes, fulltext and other useful things based off of arbitrary article URLs. Also, Metadoc is relatively fast.

## Example

You just throw it any news article URL, and Metadoc will yield.
```python
from metadoc import Metadoc
url = "https://theintercept.com/2016/11/17/iphones-secretly-send-call-history-to-apple-security-firm-says"
metadoc = Metadoc(url=url).query_all()
metadoc.return_ball()
```
=>
```json
{
  "title": "iPhones Secretly Send Call History to Apple, Security Firm Says",
  "url": "https://theintercept.com/2016/11/17/iphones-secretly-send-call-history-to-apple-security-firm-says/",
  "domain": {
    "date_registered": "2009-10-01T00:00:00",
    "credibility": {
      "is_blacklisted": false,
      "fake_confidence": "0.00"
    },
    "name": "theintercept.com",
    "favicon": "https://logo.clearbit.com/theintercept.com?size=200"
  },
  "text": {
    "contenthash": "517b04163d95c264dfffb9797b824026",
    "fulltext": "Apple emerged as a guardian of user privacy this year [...]",
    "pullquotes": [
      "Anyone else who might be able to obtain the user’s iCloud credentials, like hackers [...]",
    ],
    "reading_time": 442
  },
  "entities": {
    "keywords": {
      "apple": 1.020775623268698,
      "data": 1.0173130193905817,
      "logs": 1.0235457063711912,
      "icloud": 1.0242382271468145
    },
    "names": [
      "San Bernardino",
      "Syed Rizwan",
      "Vladimir Katalov",
      "Apple CallKit",
      "Chris Soghoian",
      "Jonathan Zdziarski"
    ]
  },
  "image": "https://prod01-cdn04.cdn.firstlook.org/wp-uploads[...]",
  "authors": [
    "Kim Zetter"
  ],
  "language": "en",
  "social": [{
    "metrics": [
      {
        "label": "sharecount",
        "count": 5994
      }
    ],
    "provider": "facebook"
  }]
}
```

## Trustworthiness Check
Since it's painful watching humans be all aggrevated about those fake news making the rounds, Metadoc does a rather crude background check on article sources. This means compiling a simple blacklist-lookup and `whois` data on the domain. Blacklists taken into account include the widely discredited [PropOrNot](http://www.propornot.com/p/the-list.html). Thus, only if a domain is found on every blacklist do we spit out a `fake_confidence` of 1. The resulting metadata should be taken with lots of salt. To put it in the words of [Don DeLillo](http://www.theparisreview.org/interviews/1887/don-delillo-the-art-of-fiction-no-135-don-delillo) – "lists are a form of cultural hysteria."

## Purpose
This humble library is used in the context of a larger news-related software undertaking. We're synthesizing what we dub "audience-evaluated content" with automated metadata. Machine-in-the-loop, if you will. Sounds like bullshit, but it's totally not. If you're intrigued and might want to work with us, feel free to drop a line to p at psolbach dot com.

## Install
Requires python 3.5.

#### Using pip
```shell
pip install metadoc
curl -L git.io/v1Muh | python3
```

## Develop

#### Mac OS
```shell
brew install python3 libxml2 libxslt libtiff libjpeg webp little-cms2
```
#### Linux
```shell
apt-get install -y python3 libxml2-dev libxslt-dev libtiff-dev libjpeg-dev webp whois
```
#### Then
```shell
pip3 install -r requirements.txt
python metadoc/__install__.py
python run.py => serving @ 6060
```

## Todo
* Page concatenation is needed in order to properly calculate wordcount and reading time.
* Authenticity heuristic with sharecount deviance detection (requires state).
* ~~Perf: Worst offender is nltk's pos tagger. Roll own w/ Average Perceptron.~~
* ~~Newspaper's summarize is doing a poor job, fulltext is slow. Move to libextract?~~

---

Metadoc stems from a pedigree of nice libraries like [libextract](https://github.com/datalib/libextract), [langdetect](https://github.com/Mimino666/langdetect) and [nltk](https://github.com/nltk/nltk).   
Metadoc leans on [this](https://github.com/hankcs/AveragedPerceptronPython) perceptron implementation inspired by Matthew Honnibal.    
Metadoc is maintained by [@___paul](https://twitter.com/___paul)   

