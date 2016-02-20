Feedlark:tm: Aggregator
================

Dependencies
------------

- Python 2.7
- pymongo
- gearman
- Feedlark Adder
- Feedlark Getter

What is this?
-------------

This is the code that ties the three Feedlark databases together, it coalesces `feed` and `user` and places the data in `g2g`.
The machine learning components will be put here eventually to decide the order of the items but for now they are sorted chronologically.

How to do tests
---------------

The tests are written with the unittest module in python.

To run them make sure you have all the dependencies and the dbtools are running then run:

	$ python testing.py


To add unit tests modify the testing.py file.
Check out the unittest docs for examples and general help.
