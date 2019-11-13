## -------------------------------------------------------- ##
#   Trab 2 IA 2019-2
#
#   Rafael Belmock Pedruzzi
#
#   zeroR.py: implementation of the ZeroR classifier.
#
#   Python version: 3.7.4
## -------------------------------------------------------- ##

import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted
from sklearn.utils.multiclass import unique_labels

class ZeroR(BaseEstimator, ClassifierMixin):
    def __init__(self):
        self.X_              = [] # data
        self.y_              = [] # data classes
        self.r_              = [] # chosen classification rule
        self.classes_        = [] # classes names

    def fit(self, X, y):
        # check that x and y have correct shape
        X, y = check_X_y(X,y)
        # store the classes seen during fit
        self.classes_ = unique_labels(y)

        self.X_ = X
        self.y_ = y

        self.r_ = np.argmax(np.bincount(y))

        # Return the classifier
        return self

    def predict(self, X):
        # Check is fit had been called
        check_is_fitted(self, ['X_', 'y_'])

        # Input validation
        X = check_array(X)

        (n,_) = X.shape
        return self.r_ * np.ones(n)


# from sklearn import datasets
# from sklearn.model_selection import train_test_split, cross_val_score

# nn = ZeroR()
# # iris = datasets.load_breast_cancer()
# iris = datasets.load_iris()
# x_train,x_test,y_train,y_test = train_test_split(iris.data,iris.target,test_size = 0.4, random_state = 0)
# nn.fit(x_train, y_train)
# y_pred = nn.predict(x_test)
# print(y_test)
# print(y_pred)
# score = cross_val_score(nn, x_train, y_train, cv = 5)
# print(score)