## -------------------------------------------------------- ##
#   Trab 2 IA 2019-2
#
#   Rafael Belmock Pedruzzi
#
#   centroid.py: implementation of the Centroid classifier.
#
#   Python version: 3.7.4
## -------------------------------------------------------- ##

import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.validation import check_X_y, check_array,check_is_fitted
from sklearn.utils.multiclass import unique_labels
from sklearn.metrics import euclidean_distances
from itertools import zip_longest
from statistics import mean
from scipy.spatial.distance import cdist

class Centroid(BaseEstimator, ClassifierMixin):

    def __init__(self):
        self.X_         = [] # data
        self.y_         = [] # data classes
        self.classes_   = [] # classes' names
        self.centroids_ = [] # classes' centroids

    def __centroid(self, xs):
        centroid = []
        for i in np.array(xs).T:
            centroid.append(mean(i))
        return centroid

    def __closest_node_index(self, node, nodes):
        return cdist([node], nodes).argmin()

    def fit(self, X, y):
        # check that x and y have correct shape
        X, y = check_X_y(X,y)
        # store the classes seen during fit
        self.classes_ = unique_labels(y)

        self.X_ = X
        self.y_ = y

        centroids = []
        xy = list(zip_longest(X,y))
        for i in range(len(np.unique(y))):
            c = [t[0] for t in xy if t[1] == i] # all elements of class i
            centroids.append(self.__centroid(c))
        self.centroids_ = centroids

        # Return the classifier
        return self

    def predict(self, X):
        # Check is fit had been called
        check_is_fitted(self, ['X_', 'y_'])

        # Input validation
        X = check_array(X)

        y = []
        for i in X:
            c = self.__closest_node_index(i,self.centroids_)
            y.append(self.classes_[c])
        return y

# from sklearn import datasets
# from sklearn.model_selection import train_test_split, cross_val_score
# from sklearn.metrics import f1_score

# nn= Centroid()
# iris = datasets.load_iris()
# x_train,x_test,y_train,y_test = train_test_split(iris.data,iris.target,test_size = 0.4, random_state = 0)
# nn.fit(x_train, y_train)
# y_pred = nn.predict(x_test)
# print(y_test)
# print(y_pred)
# score = cross_val_score(nn, x_train, y_train, cv = 5)
# print(score)
