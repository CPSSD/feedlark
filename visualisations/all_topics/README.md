Visualisation: All Topics
=========================

This module will output statistics about the interest of all users in certain topics.

Dependencies
------------

- Python 2.7

How to do tests
------------

The tests are written with the unittest module in python.

Move to this directory, and run `python testing.py` to run the unit tests.

To add unit tests modify the testing.py file.
Check out the unittest docs for examples and general help.

Usage
-----

Run `python all_topics.py X`, where X is the number of topics you want the program to output data on. If this number is larger than the total number of topics, the program will output data for every topic in the database.

The first line of the output is the number of users in the system. The second line is the number of topics in the whole dataset, followed by the number of lines remaining in the output.

The program will then output a series of lines, with a single topic on each line followed by the number of users who have that topic in their list of opinions, the mean value, the mode value, and the median value of the opinion of that topic across those users. All values are separated by a single space. If there is no mode value, an `X` will be printed. The output will be sorted by the number of users who have an opinion on each topic, in descending order.

```
100
17 3
animals 100 2.2 3 2
dogs 89 5.7 5 7
dolphins 34 -1.22 X -1
```

All of this data is computed at run-time, and is not cached, so might take some time.
