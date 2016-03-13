Feedlark:tm: Scraper
================

Dependencies
------------

- Python 2.7
- pip
- virtual environment
- requests
- feedparser
- BeautifulSoup

How to set up your environment
------------------------------

I recommend you setup a virtual env before you download the dependencies.

    $ pip install virtualenv
    $ cd ./scraper/
    $ virtualenv venv
    $ # On Posix Systems
    $ . venv/bin/activate
    $ # Windows Activation
    $ venv\Scripts\activate
    $ # When you're done run:
    $ deactivate


This will give you a clean slate to manage dependencies, making sure that
there is no overlap.

Use pip to download the dependencies (making sure you have activated the
virtualenv).

Depends are in the root script directory.

    $ pip install -r script/requirements.txt


How to do tests
------------

The tests are written with the unittest module in python.

To run them make sure you are in the virtualenv (so you have all the dependencies) and run:

	$ python -m unittest


To add unit tests modify the testing.py file.
Check out the unittest docs for examples and general help.
