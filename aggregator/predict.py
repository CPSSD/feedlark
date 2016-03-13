# The tool to predict how much interest a user will have in an article

from sklearn import linear_model

class Regression:
    model = None

    def __init__(self):
        self.model = linear_model.SGDClassifier(loss="log") # loss="log" makes it use logistic regression

    def train(self, x, y):
        self.model.fit(x, y)

    def predict(self, x):
        probs = [a[0] for a in self.model.predict_proba(x)]
        ans = self.model.predict(x)
        print(probs)
        print(ans)
        

if __name__ == '__main__':
    reg = Regression()
    reg.train([[1, 2], [1, -1]], [0, 1])
    reg.predict([[1,2]])
    reg.predict([[2,-3]])
    reg.predict([[1,-7]])
    reg.predict([[1,0]])
