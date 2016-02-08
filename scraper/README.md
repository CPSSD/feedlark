Feedlark:tm: Scraper
================

Dependencies
------------

- Python 3.5
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
    $ virtualenv -p "~path of your python3 executable~" venv
    $ # On Posix Systems
    $ . venv/bin/activate
    $ # Windows Activation
    $ venv\Scripts\activate
    $ # When you're done run:
    $ deactivate


This will give you a clean slate to manage dependencies, making sure that
there is no overlap.

Use pip to download the dependencies (making sure you have activated the
virtualenv)

    $ pip install -r requirements.txt


How to do tests
------------

Coming soon to a repo near you!