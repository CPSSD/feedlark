Feedlark Database Getter
========================

Dependencies
------------

- Python 2.7
- [Pymongo 3.2.1](https://github.com/mongodb/mongo-python-driver)
- [Python-Gearman 2.0.2](https://pypi.python.org/pypi/gearman)

How to set up your environment
------------------------------

```python
pip install gearman

git clone https://github.com/mongodb/mongo-python-driver
python setup.py install
```

Don't install another BSON lib, pymongo comes with its own one.

How to do tests
---------------

`python ../dbtools_test.py`

How to use
----------

All communications are done in BSON. It expects data formatted as follows. The 'projection' field is optional.

```js
{
    "database": "feedlark",
    "collection": "user",
    "query": {
        "email":"cian.ruane9@mail.dcu.ie"
    }, 
    "projection": {
        "_id": 1,
        "email": 1 
    }
}
```

And returns, in BSON, a list of documents that match; it may be an empty list.
It also has a "status" field, which will be set to "error" in the case that something goes wrong.

```js
{
    "docs": [
        {
            "_id": ObjectId(123456789012)
        },
        {
            "_id": ObjectId(133790014242)
        }
    ],
    "status":"ok"
}
```
