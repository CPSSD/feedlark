feedlark web application
========================

Requires
--------

- Node.js to be installed.
Recommended v4.0.0 or up, but I think 0.10 and up will do.
- NPM to be installed

Usage
-----

```sh
# Install server depends locally in server/node_packages
cd server && npm install

# Run the server
PATH=$(npm bin):$PATH sails lift
# Hold up! That looks kind of annoying to type a lot
# To make this easier, add an alias in your ~/.bashrc (or whereever else it is)
# alias npm-exec='PATH=$(npm bin):$PATH'

# Run the tests when they are written
# npm run tests
```
