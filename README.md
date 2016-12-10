# Doxhund
[![Build Status](https://travis-ci.org/psolbach/doxhund.svg?branch=master)](https://travis-ci.org/psolbach/doxhund)
[![Coverage Status](https://coveralls.io/repos/github/psolbach/doxhund/badge.svg?branch=master)](https://coveralls.io/github/psolbach/doxhund?branch=master)  

Doxhund is a post-truth era news article metadata retrieval service and API mashup. It does social media activity lookup, source authenticity rating, checksum creation, json-ld and metatag parsing as well as information extraction for named entities, pullquotes, fulltext and other useful things based off of arbitrary article URLs. Also, doxhund retrieves relatively fast.
It wants to be pronounced "dachshund".

## Example

You just throw it any news article URL, and Doxhund will yield.
```python
from doxhund import Doxhund
url = "https://theintercept.com/2016/11/17/iphones-secretly-send-call-history-to-apple-security-firm-says"
doxhund = Doxhund(url=url).query_all()
doxhund.return_ball()
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
Since it's painful to watch the beloved humans be all aggrevated about those fake news making the rounds, Doxhund does a rather crude background check on article sources. This means e.g. a simple blacklist-lookup and `whois` on the domain. Blacklists taken into account include the widely discredited [PropOrNot](http://www.propornot.com/p/the-list.html). The whole concept is very much alarming in itself. Thus, only if a domain is found on every blacklist do we spit out a `fake_confidence` of 1. That means we are conservative here. The resulting metadata should be taken with lots of saltgrains. Let's put it like [Don DeLillo would](http://www.theparisreview.org/interviews/1887/don-delillo-the-art-of-fiction-no-135-don-delillo) – because "lists are a form of cultural hysteria." 

## Install
Requires python 3.5.

#### Using pip
```shell
pip install doxhund
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
curl https://raw.githubusercontent.com/codelucas/newspaper/master/download_corpora.py | python3
python -m nltk.downloader averaged_perceptron_tagger words maxent_ne_chunker
python run.py => serving on port 6060
```

## Todo
* Newspaper's summarize is doing a poor job, maybe python-goose, polyglot, dat/pyner can help.
The results of summarize are used as pullquote suggestions for now.
* Page concatenation is needed in order to properly calculate wordcount and reading time.
* Authenticity heuristic with sharecount deviance detection (requires state).

---

Doxhund stems from a pedigree of nice libraries like [newspaper](https://github.com/codelucas/newspaper), [nltk](https://github.com/nltk/nltk) and [langdetect](https://github.com/Mimino666/langdetect).   
Doxhund is maintained by [@___paul](https://twitter.com/___paul)   

