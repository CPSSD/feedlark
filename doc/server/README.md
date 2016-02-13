Feedlark Web Server
======

Goals:
------

- Prototype first, perfect later
- Make it fast
- Make it modular so we can make cooler stuff later
- Follow an MVC convention

What we considered
-------------------

- Django
  - Very large community
  - Great documentation
  - Lacking relational database support
- Flask
  - Fast and modular
  - Awkward daemoning due to odd uWSGI tools.
  - Very loose in terms of MVC
- Express.js
  - Great documentation
  - Great community
  - Very modular
  - A little barebones in terms of testing information
  - Loose MVC
- Sails.js
  - Based on Express.js
  - Stronger MVC basis
  - Database ORM and a supported MongoDB library
  - Very fast to prototype

Final Decision
--------------

- Sails with `sails-mongo`
