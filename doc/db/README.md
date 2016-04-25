DB Documentation
================

General Info
------------

We decided on using a *NoSQL database* because it suited our data type well, and
because we needed modify feeds independently quickly.

We settled on using [MongoDB](https://github.com/mongodb/mongo) because of it's
great performance and real world usage.

Configuration
-------------

Development configuration is stored in `script/mongodb/mongodb.conf`.

The port was changed to `9001` to help subdue automated port based attacks.

Anything that connects to the database uses an environment variable named
`ENVIRONMENT` to decide whether to use authentication.

XXX: Currently this database password is in the source repository. This
behaviour should be modified soon.
