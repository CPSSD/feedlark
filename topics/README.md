Feedlark Topic Modeller
=======================

This is the module for grabbing the topics out of an article. Right now, we just use a method where we take the words that come up the most commonly in an article, and then remove stop words (ie. Words that carry no meaning, function words).

This worker takes in a specific article to get the topics of, and then updates the `feed` database with this information.

Setup
-----

The following libraries are required:

- [Gearman](https://pypi.python.org/pypi/gearman)
- [Pymongo](http://api.mongodb.org/python/current/installation.html) - only uses it for its bson library
- [spacy](http://spacy.io/#install)

The worker must use Python 2, as Gearman does not support python 3.

Spacy requires the following before it is installed:

`sudo apt-get install build-essential python-dev` 

This is detailed in the install instructions linked above.

It will also be necessary to download Spacy's English model with the following command:

`python -m spacy.en.download`

It downloads about 500mb of data.

All of these procedures are included in the Vagrantfile.

Usage
-----

The tool takes in Gearman data in the following format:

```js
{
    "article": "lorem ipsum dolor sit amet",
    "_id": ObjectId(000000000000),
    "link": "http://dave.cheney.net/2016/02/06/unhelpful-abstractions"
}
```

`article` should contain the text of the post to be analysed. `_id` must be the id of the document in the `feed` collection. `link` should be the link to that specific article, so that this worker can update just the entry for this article without modifying any of the other articles in the document specified by `_id`.


It returns the following:

```js
{
    "status":"ok",
    "topics":{
        "lorem":0.5,
        "ipsum":0.25,
        "dolor":0.25
    }
}
```

The `topics` field will contain an arbitrary number of entries; it cannot be assumed that there will be any particular number of topics.

Each of the float values associated with each topic is the ratio of that word and the total number of content words in the article, not the ratio of that word and the words in the returned topics. That means that the float values of all topics in the returned list will not add up to one, if there are more topics in the article than the max number returned.
