# The tool to predict how much interest a user will have in an article

import pickle 
import gearman
from datetime import datetime
from sklearn import linear_model

def log(*message, **kwargs):
    '''
    Logs to stdout

    Pass in parameters as you would the python3 print function.
    Includes the optional 'level' keyword argument, defaults to 0.
    '''
    level = kwargs['level'] if 'level' in kwargs else 0
    levels = ['INFO:', 'WARNING:', 'ERROR:']

    message_str = ''.join(map(str, message))
    time = str(datetime.now()).replace('-', '/')[:-7]

    print time, levels[level], message_str


class Classification:
    model = None

    def __init__(self):
        # loss="log" makes it use logistic regression
        self.model = linear_model.SGDClassifier(loss="log", n_iter=5)

    def predict(self, x):
        """expects a list of lists representing each of the sets of inputs to be classified.
        outputs a list of floats, with how likely it is the given input set will be in 'liked' category"""

        print x

        #this is a list of list, where the outer list is the data for each input,
        #and the inner list is how likely that input will match each class
        probabilities = self.model.predict_proba(x)

        print probabilities

        print 'predict', self.model.predict(x)

        #get how likely each input will match the second class (index 1), ie. a 'like'
        probabilities_of_like = [a[1] for a in probabilities]
        
        print probabilities_of_like
        return probabilities_of_like

    def load_model(self, pickled_model):
        log('Loading pickled model.')
        self.model = pickle.loads(pickled_model) 
    
    def train(self, x, y):
        # not called except in testing, the training actually happens in /refresh_model
        log('Training model')
        self.model.fit(x, y)
    
if __name__ == '__main__':
    c = Classification()
    c.train([[1., 5.], [2., -5.], [2., 7.], [1., -3.], [1.,0.], [1.0, -0.1]], [0, 1, 0, 1, 0, 1])
    print c.predict([[1., 10.]])
    print c.predict([[2., 4.]])
    print c.predict([[3., -10.]])
    print c.predict([[-1., 1.1]])
    print c.predict([[1.0, -3.0]])
    print c.predict([[1.2, -2.1]])
