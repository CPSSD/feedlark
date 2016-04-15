Machine Learning Methods
========================

Our number one concern is speed of deployment, as we do not want to get bogged down in the theory of machine learning; that could take months or years to understand and implement.

As such, we chose to use an off-the-shelf solution. We considered several options, such as `SmileMiner` (Java), `Apache Spark` (Scala, Java, Python) and `Orange` (Python), however, we chose to use `scikit-learn` for the following reasons:

- It is in Python, so it is accessable to any member of the team
- It is a mature, well-supported and fully-featured library
- It has support for on-line learning models

We are using scikit-learn's `SGDClassifier` class, for which the documentation is [here](http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html). We train it with two classes, whether a user is "interested" or "not interested" in that article. The inputs are:

- A measure of the similarity in topics between the article and the user's interests (from `kw_score.py`)
- The age of the article

If a user upvotes an article, these inputs are mapped to a value of 1. If they downvote an article, these inputs are mapped to a value of -1. 

When we add some data to the model, it is pickled and put in the `user` db collection. This is done by the `update-user-model` Gearman worker.

