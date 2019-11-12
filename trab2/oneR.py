## -------------------------------------------------------- ##
#   Trab 2 IA 2019-2
#
#   Rafael Belmock Pedruzzi
#
#   oneR.py: implementation of the OneR classifier.
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

class OneR(BaseEstimator, ClassifierMixin):
    def __init__(self):
        self.X_              #
        self.y_              #
        self.r_              #
        self.classes_        #
        self.kbd_            #
        self.class_selector_ #
    
    # def get_params(self, deep=True):
    #     return super().get_params(deep)

    def fit(self, X, y):
        # check that x and y have correct shape
        X, y = check_X_y(X,y)
        # store the classes seen during fit
        self.classes_ = unique_labels(y)

        self.y_ = y

        kbd = KBinsDiscretizer(n_bins = len(np.unique(y)), encode='ordinal')
        X = kbd.fit_transform(X)
        self.X_ = X
        self.kbd_ = kbd

        cm_list = []
        hits = []
        for i in X.T:
            cm = contingency_matrix(i, y)
            cm_list.append(cm)
            hits.append(sum(max(k) for k in cm))

        rule = np.argmax(hits) # chosen rule
        self.r_ = rule

        rule_cm = cm_list[rule]
        class_selector = []
        for i, c in enumerate(rule_cm.T):
            p = np.argmax(c)
            class_selector.append(p)
        self.class_selector_ = class_selector

        # Return the classifier
        return self

    def predict(self, X):
        # Check is fit had been called
        check_is_fitted(self, ['X_', 'y_'])

        # Input validation
        X = check_array(X)

        X = self.kbd_.transform(X)

        y = []
        for i in X[:,self.r_]:
            y.append(self.class_selector_[int(i)])

        return y


from sklearn import datasets
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import f1_score

nn= OneR()
iris = datasets.load_iris()
x_train,x_test,y_train,y_test = train_test_split(iris.data,iris.target,test_size = 0.4, random_state = 0)
nn.fit(x_train, y_train)
y_pred = nn.predict(x_test)
print(y_test)
print(y_pred)
score = cross_val_score(nn, x_train, y_train, cv = 5)
print(score)
