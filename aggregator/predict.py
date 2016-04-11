# The tool to predict how much interest a user will have in an article

import pickle 
import gearman
from sklearn import linear_model

class Classification:
    model = None

    def __init__(self):
        # loss="log" makes it use logistic regression
        self.model = linear_model.SGDClassifier(loss="log")

    def predict(self, x):
        """expects a single flat list, x, the inputs for the prediction.
        outputs a single float, how likely it is the article will be in 'liked' category"""

        print x

        #this is a list of list, where the outer list is the data for each input,
        #and the inner list is how likely that input will match each class
        probabilities = self.model.predict_proba(x)

        print probabilities

        #get how likely each input will match class 0, ie. a 'like'
        probabilities_of_like = [a[0] for a in probabilities]
        
        print probabilities_of_like
        return probabilities_of_like

    def load_model(self, pickled_model):
        self.model = pickle.loads(pickled_model) 
        
    def train(self, x, y):
        self.model.partial_fit(x, y, classes=[0, 1])

if __name__ == '__main__':
    c = Classification()
    c.train([[1, 5], [2, -5], [2, 7], [1, -3], [1,0]], [0, 1, 0, 1, 0])
    print c.predict([[1, 10]])
    print c.predict([[2, 4]])
    print c.predict([[3, -10]])
    print c.predict([[-1, 11]])
