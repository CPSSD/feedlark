Feedlark Backend CLI
=========================

This module allows you to make requests to the backend Gearman workers in a nice way.

Dependencies
------------

- Python 2.7
- bson
- gearman

How to do tests
------------

The tests are written with the unittest module in python.

Move to this directory and run `python testing.py` to start the unit tests.

To add unit tests modify the testing.py file.
Check out the unittest docs for examples and general help.

Usage
-----

Run `python cli.py`, the interface will guide you throught the rest.

**Note:**
When inputting the key: value pairs for arbitrary dicts (e.g. the selector in `db-upsert`) the input is taken literally, so use `'url': 'abc.com'` rather than `url: abc.com`.

Adding new workers
------------------

To add a new worker simply add a new class in workers.py.

I recommend following this template:
```python
@standard_response
@standard_error
class TemplateWorker:
    NAME = 'gm-worker-name'
    NICENAME = 'Name For Menu'
    REQUEST = {
        'key': str,
        'url': str,
    }
```

Remember to change the class name but keep 'Worker' at the end!

The request dict defines the structure of your request, as of now the CLI only supports dicts as containers, trying to send a list or set is undefined behaviour.
The actual values taken in by the CLI will be cast to whatever type you include as the values in the `REQUEST` dict, therefor you need to make sure you use `str` rather than `''`, unit tests will catch that though.

If your worker doesn't return `{'status': 'error', 'description': 'Cosmic rays'}` on error then don't include the `@standard_error` decorator and write your own error functions, you can see how they are implemented in decorators.py

If your worker doesn't return a dictionary at all then you will also have to remove the `@standard_response` decorator and overload the `print_response` function in your class. Again, an example can be seen in decorators.py
