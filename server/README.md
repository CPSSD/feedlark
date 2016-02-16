feedlark web application
========================

Requires
--------

- Node.js to be installed. Recommended `v4.0.0` or up.

- NPM to be installed.

Install
-------

If you are using Vagrant, this should be done.

If you are not, then inside `/server` run:

```sh
$ npm install -y
```

Usage
-----

To execute the various commands of the server, use `npm run`.

Here's a list of what you can do:

| command         | notable details                                           |
| ------          | ---------------                                           |
| `npm run start` | starts the sail server, using `sails lift`.               |
| `npm run tests` | starts the mocha.js tests located in `tests/`             |

Here's a list of what we _maybe should_ be able to do:

| command         | notable details                                           |
| ------          | ---------------                                           |
| `npm run irl`   | starts the sail server with configuration for deployment  |
| `npm run lint`  | lint everything                                           |
