Feedlark Topic Modeller
=======================

This is the module for grabbing the topics out of an article. Right now, we just use a method where we take the words that come up the most commonly in an article, and then remove stop words (ie. Words that carry no meaning, function words).

Setup
-----

The following libraries are required:

- [Gearman](https://pypi.python.org/pypi/gearman)
- [Pymongo](http://api.mongodb.org/python/current/installation.html) - only uses it for its bson library
- [spacy](http://spacy.io/#install)

The worker must use Python 2, as Gearman does not support python 3.

It will also be necessary to download Spacy's English model with the following command:

`python -m spacy.en.download`

It downloads about 500mb of data.

Usage
-----

The tool takes in Gearman data in the following format:

```js
{
    article: "lorem ipsum dolor sit amet"
}
```

It returns the following:

```js
{
    "status":"ok",
    "topics":["lorem", "ipsum"]
}
```

The `topics` field will contain a list of arbitrary length; it cannot be assumed that there will be any particular number of topics.

