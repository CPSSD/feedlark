Feedlark:tm: Scraper
================

This module gets the error of a given user's prediction model.

It uses the '2-fold cross-validation' method, as described [here](https://en.wikipedia.org/wiki/Cross-validation_%28statistics%29#2-fold_cross-validation)

Dependencies
------------

- Python 2.7
- scikit-learn
- gearman

How to Test
-----------

Move to this directory, and run `python testing.py`.

Usage
-----

Use `source /home/python/bin/activate` to set the Python environment.

To get the error of a user's model, just then run `python model_error.py <username>`.

