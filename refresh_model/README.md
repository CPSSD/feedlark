Refresh Model
=============

What is this?
-------------

This is a Gearman worker that, when given a user, looks through the `vote` collection in the database for all votes made by that user, and creates a new classification model for them, putting it in their document in the `user` collection.

Usage
-----

The worker is called `refresh-model`, and takes the following Gearman input data:

```js
{
    "key": "secret_key_abc",
    "username": "sully"
}
```

The `username` field is optional. If it is not supplied, the worker will operate upon all users. 

It outputs either:

```js
{
    "status": "success"
}
```

or

```js
{
    "status": "error",
    "description": "error description"
}
```

How to do tests
---------------

To run the tests, move to this repository, and run:

`$ python testing.py`

To add a test, modify the `testing.py` file.
