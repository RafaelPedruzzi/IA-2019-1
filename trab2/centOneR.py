## -------------------------------------------------------- ##
#   Trab 2 IA 2019-2
#
#   Rafael Belmock Pedruzzi
#
#   centOneR.py: implementation of the Centroid OneR classifier.
#
#   Python version: 3.7.4
## -------------------------------------------------------- ##

import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted
from sklearn.utils.multiclass import unique_labels
from sklearn.metrics import euclidean_distances
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.metrics.cluster import contingency_matrix
from sklearn.metrics import confusion_matrix
from itertools import product, zip_longest
from statistics import mean
from scipy.spatial.distance import cdist

class Centroid_OneR(BaseEstimator, ClassifierMixin):

    # def __init__(self):

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

        self.y_ = y

        kbd = KBinsDiscretizer(n_bins = len(np.unique(y)), encode='ordinal')
        dX = kbd.fit_transform(X) # discretized X
        self.X_ = dX
        self.kbd_ = kbd

        cm_list = []
        hits = []
        for i in dX.T:
            cm = contingency_matrix(i, y)
            cm_list.append(cm)
            hits.append(sum(max(k) for k in cm))

        rule = np.argmax(hits) # chosen rule
        self.r_ = rule

        rule_cm = cm_list[rule]
        class_selector = []
        for i, c in enumerate(rule_cm):
            p = np.argmax(c)
            class_selector.append(self.classes_[p])

        ny = []
        for i in dX[:,rule]:
            ny.append(class_selector[int(i)])

        centroids = []
        xy = list(zip_longest(X,ny))
        for i in range(len(np.unique(ny))):
            c = [t[0] for t in xy if t[1] == i] # all elements of class i
            centroids.append(self.__centroid(c))
        self.centroids = centroids

        # Return the classifier
        return self

    def predict(self, X):
        # Check is fit had been called
        check_is_fitted(self, ['X_', 'y_'])

        # Input validation
        X = check_array(X)

        y = []
        for i in X:
            c = self.__closest_node_index(i,self.centroids)
            y.append(self.classes_[c])
        return y


# from sklearn import datasets
# from sklearn.model_selection import train_test_split, cross_val_score
# from sklearn.metrics import f1_score

# nn= Centroid_OneR()
# iris = datasets.load_breast_cancer()
# x_train,x_test,y_train,y_test = train_test_split(iris.data,iris.target,test_size = 0.4, random_state = 0)
# nn.fit(x_train, y_train)
# y_pred = nn.predict(x_test)
# print(y_test)
# print(y_pred)
# score = cross_val_score(nn, x_train, y_train, cv = 5)
# print(score)
