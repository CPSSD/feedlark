User Database Specifications
===========================

The user database is the database that holds data individual to each user,
including authentication data  and is used in combination with the Feed
Database to create entries in the finished G2G database.

The user password will not be stored, instead, a salt and the hashed password
and salt will be stored. These are stored in the same string in bcrypt.

Tokens
-------

Tokens represents the randomly generated API tokens. Currently they point to a
true value but this could be modified such that each token had validation date
and permissions.

Models
-------

The `model` field holds a pickled scikit-learn `SGDClassifier`, ie. the
classification model of that user. It is compiled from the data in the other
fields, and is updated by the `update-user-model` Gearman worker.

Verification
-------

When the user initially signs up, `verified` will be a token used to
verify the address from the link in the email. It will be set to `true`
permanently after verification.

Config
------

Users have a set of default behaviour that they can set and these are stored
in the `defaults` key.

#### Current Defaults:

```
{
	 // this refers to the default pagination size
	"page_length": int
}
```

Example Document
----------------


```js
{
	"_id": ObjectId("5099803df3f4948bd2f98391"),
	"username": "iandioch",
	"email": "noah@feedlark.com",
	"verified": true,
	"password": "$2a$08$ThzPc3zm84JPb6LmvcfCkuXkwyh8H.Mn1VC4EKu9guksI9lbdb7Fa",
	"subscribed_feeds": ["news.ycombinator.com/rss", "pssd.computing.dcu.ie/rss.xml"],
	"words": {"butter":2, "milk":13, "antidisestablishmentarianism":-33},
	"defaults": {"page_length": 20}
	"tokens": {"add15f620657bb3fd8ce7fa9611f1aaba8717559295706a6d80f9e8cf58e81d7":true},
	"model": "ccopy_reg\n_reconstructor\np0\n(csklearn.linear_model.stochastic_gradient\nSGDClassifier\np1\nc__builtin__\nobject\np2\nNtp3\nRp4\n(dp5\nS't_'\np6\ncnumpy.core.multiarray\nscalar\np7\n(cnumpy\ndtype\np8\n(S'f8'\np9\nI0\nI1\ntp10\nRp11\n(I3\nS'<'\np12\nNNNI-1\nI-1\nI0\ntp13\nbS'\\x00\\x00\\x00\\x00\\x00\\x98\\x8f@'\np14\ntp15\nRp16\nsS'n_jobs'\np17\nI1\nsS'shuffle'\np18\nI00\nsS'verbose'\np19\nI0\nsS'classes_'\np20\ncnumpy.core.multiarray\n_reconstruct\np21\n(cnumpy\nndarray\np22\n(I0\ntp23\nS'b'\np24\ntp25\nRp26\n(I1\n(I2\ntp27\ng8\n(S'i8'\np28\nI0\nI1\ntp29\nRp30\n(I3\nS'<'\np31\nNNNI-1\nI-1\nI0\ntp32\nbI00\nS'\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\x00\\x00\\x00\\x00'\np33\ntp34\nbsS'class_weight'\np35\nNsS'fit_intercept'\np36\nI01\nsS'penalty'\np37\nS'l2'\np38\nsS'random_state'\np39\nNsS'loss_function'\np40\ncsklearn.linear_model.sgd_fast\nLog\np41\n(tRp42\nsS'C'\np43\nF1.0\nsS'n_iter'\np44\nI5\nsS'epsilon'\np45\nF0.1\nsS'learning_rate'\np46\nS'optimal'\np47\nsS'coef_'\np48\ng21\n(g22\n(I0\ntp49\ng24\ntp50\nRp51\n(I1\n(I1\nI2\ntp52\ng8\n(S'f8'\np53\nI0\nI1\ntp54\nRp55\n(I3\nS'<'\np56\nNNNI-1\nI-1\nI0\ntp57\nbI00\nS\"\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\xdd}'\\xb4\\x00\\x94\\xd3\\xc2\"\np58\ntp59\nbsS'alpha'\np60\nF0.0001\nsS'intercept_'\np61\ng21\n(g22\n(I0\ntp62\ng24\ntp63\nRp64\n(I1\n(I1\ntp65\ng11\nI00\nS'\\x00\\x00\\x00\\x00\\x00\\x00\\x14\\xc0'\np66\ntp67\nbsS'_expanded_class_weight'\np68\ng21\n(g22\n(I0\ntp69\ng24\ntp70\nRp71\n(I1\n(I2\ntp72\ng11\nI00\nS'\\x00\\x00\\x00\\x00\\x00\\x00\\xf0?\\x00\\x00\\x00\\x00\\x00\\x00\\xf0?'\np73\ntp74\nbsS'warm_start'\np75\nI00\nsS'loss'\np76\nS'log'\np77\nsS'eta0'\np78\nF0.0\nsS'l1_ratio'\np79\nF0.15\nsS'power_t'\np80\nF0.5\nsb."
}
```

The above document uses the following data to generate the hashed password:

		password = "ilovegnuhurd", 8 rounds
