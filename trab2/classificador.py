from sklearn.base import BaseEstimato, ClassifierMixin
from sklearn.utils.validation import check_X_y, check_array,check_is_fitted
from sklearn.utils.multiclass import unique_labels
from sklearn.metrics import euclidian_distances

class NearestNeighborClassifier(BaseEstimator, ClassifierMixin):

    def __init__(self, demo_param='demo'):
        self.demo_param = demo_param

    def fit(self, X, y):
        # check that x and y have correct shape
        X, y = check_X_y(X,y)
        # store the classes seen during fit
        self.classes_ = unique_labels(y)

        self.X_ = X 
        self.y_ = y
        # Return the classifier
        return self

    def predict(self, X):
        # Check is fit had been called
        # check_is_fitted(self)

        # Input validation
        X = check_array(X)

        closest = np.argmin(euclidian_distances(X,self.X_), axis=1)
        return self.y_[closest]
 
