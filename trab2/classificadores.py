import numpy as np
import sklearn as sk
import pandas as pd
from sklearn import datasets
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted
from sklearn.utils.multiclass import unique_labels
from sklearn.metrics import euclidean_distances
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import f1_score
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.metrics.cluster import contingency_matrix
from sklearn.metrics import confusion_matrix

class ZeroR(BaseEstimator, ClassifierMixin):
    # def __init__(self, demo_param='demo'):
    #     self.demo_param = demo_param
    
    # def get_params(self, deep=True):
        # return super().get_params(deep)

    def fit(self, X, y):
        X, y = check_X_y(X, y)
        self.classes_ = unique_labels(y)

        self.c = np.argmax(np.bincount(y))

    def predict(self, X):
        (n,_) = X.shape
        return self.c * np.ones(n)


# 1- Discretizar (Número de intervalos = Número de Classes)
# 2- Tabela de Contingência
# 3- Escolha do melhor atributo  
# 4- Elaborar Regras OneR

#Parece bom
#For each attribute A:
#      For each value V of that attribute, create a rule:
#        1. count how often each class appears
#        2. find the most frequent class, c
#        3. make a rule "if A=V then C=c"
#      Calculate the error rate of this rule
#    Pick the attribute whose rules produce the lowest error rate
class OneR(BaseEstimator, ClassifierMixin):
    # def __init__(self, demo_param='demo'):
    #     self.demo_param = demo_param
    
    def get_params(self, deep=True):
        return super().get_params(deep)

    def fit(self, X, y):
        X, y = check_X_y(X, y)
        self.classes_ = unique_labels(y)

        disc = KBinsDiscretizer(n_bins = len(np.unique(y)), encode='ordinal', strategy = 'quantile')
        X = disc.fit_transform(X)

        #Iterando em cima de cada característica 
        #Falta determinar as classes para que então possamos verificar qual a mais frequente
        # vamos usar o crosstab do pandas
        X_ = []
        ct_list = []
        valores = []
        for i,j in enumerate(X.T):
            cname = 'feat-'+str(i)
            ct = pd.crosstab(j, y)
            ct_list.append(ct)
            soma = sum(max(list(ct.loc[k,:])) for k in range(ct.shape[1]))
            valores.append(soma)
        self.c = np.argmax(valores)                            
    

    def predict(self, X):
        (n,m) = X.shape
        # return self.c * np.ones(n) 

nn= OneR()
iris = datasets.load_iris()
x_train,x_test,y_train,y_test = train_test_split(iris.data,iris.target,test_size = 0.4, random_state = 0)
nn.fit(x_train, y_train)
print(y_train)


# nn = ZeroR()

# iris = datasets.load_breast_cancer()
# x_train,x_test,y_train,y_test = train_test_split(iris.data,iris.target,test_size = 0.4, random_state = 0)
# nn.fit(x_train, y_train)
# y_pred = nn.predict(x_test)
# print(y_test)
# print(y_pred)
# score = cross_val_score(nn, x_train, y_train, cv = 5)
# print(score)