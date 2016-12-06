# Doxhund
Doxhund is a postmodern news article metadata retrieval service and API mashup. It does social media activity lookup, source authenticity rating, checksum creation, json-ld and metatag parsing as well as information extraction for named entities, pullquotes, fulltext and other useful things based off of arbitrary article URLs. Also, docshund retrieves relatively fast.

# Install
Requires python 3.5.

```
brew install python3 libxml2 libxslt libtiff libjpeg webp little-cms2
virtualenv -p python3 venv; . venv/bin/activate
pip3 install -r requirements.txt
curl https://raw.githubusercontent.com/codelucas/newspaper/master/download_corpora.py | python3
python -m nltk.downloader averaged_perceptron_tagger words maxent_ne_chunker
python run.py => serving on port 6060
```

# Tests
Testing is done via pytest and asynctest.
Invoke with `py.test -v tests`

# Todo
* Profiling w/ snakeviz
* Newspaper's summarize is doing a poor job, maybe python-goose, polyglot, dat/pyner can help.
The results of summarize are used as pullquote suggestions for now.
* Page concatenation is needed in order to properly calculate wordcount and reading time.
* Authenticity heuristic in addition to user flagging, quartile sharecount detection (requires state).
