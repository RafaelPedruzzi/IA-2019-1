## -------------------------------------------------------- ##
#   Trab 2 IA 2019-2
#
#   Rafael Belmock Pedruzzi
#
#   Python version: 3.7.4
## -------------------------------------------------------- ##

from zeroR import ZeroR
from oneR import OneR
from probOneR import Prob_OneR
from centroid import Centroid
from centOneR import Centroid_OneR
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn import datasets
# from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score
from seaborn import boxplot
from statistics import mean, stdev
from matplotlib import pyplot as plt
from itertools import zip_longest
import tabulate

iris = datasets.load_iris()
digits = datasets.load_digits()
wine = datasets.load_wine()
cancer = datasets.load_breast_cancer()

DATA = [
    # Iris
    ('Iris',                        # name
    iris),            # data
    # Digits
    ('Digits',                      # name
    digits),          # data
    # Wine
    ('Wine',                        # name
    wine),            # data
    # Breast Cancer
    ('Breast Cancer',               # name
    cancer)    # data
]

CLASSIFIERS = [
    # 0- ZeroR
    (   'ZeroR',                    # classifier name
        ZeroR,                      # classifier class
        [],                         # hiperparameters
        []),                        # test parameters
    # 1- OneR
    (   'OneR',                     # classifier name
        OneR,                       # classifier function
        [],                         # hiperparameters
        []),                        # test parameters
    # 2- Probabilistic OneR
    (   'Probabilistic OneR',       # classifier name
        Prob_OneR,                  # classifier function
        [],                         # hiperparameters
        []),                        # test parameters
    # 3- Centroid
    (   'Centroid',                 # classifier name
        Centroid,                   # classifier function
        [],                         # hiperparameters
        []),                        # test parameters
    # 4- Centroid OneR
    (   'Centroid OneR',            # classifier name
        Centroid_OneR,              # classifier function
        [],                         # hiperparameters
        []),                        # test parameters
    # 5- Gaussian Naive Bayes
    (   'Gaussian Naive Bayes',     # classifier name
        GaussianNB,                 # classifier class
        [],                         # hiperparameters
        []),                        # test parameters
    # 6- Knn
    (   'Knn',                      # classifier name
        KNeighborsClassifier,       # classifier class
        [[1, 3, 5, 7, 10]],         # number of neighbors
        []),                        # test parameters
    # 7- Decision Tree
    (   'Decision Tree',            # classifier name
        DecisionTreeClassifier,     # classifier class
        [[None, 3, 5, 10]],         # maximum depth
        []),                        # test parameters
    # 8- Multi-Layer Perceptron
    (   'Multi-Layer Perceptron',   # classifier name
        MLPClassifier,              # classifier class
        [[50, 100, 200],            # maximum number of iterations
        [(15,)]],                   # hidden layer sizes
        []),                        # test parameters
    # 9- Random Forest
    (   'Random Forest',            # classifier name
        RandomForestClassifier,     # classifier class
        [[10, 20, 50, 100]],        # number of estimators
        [])                         # test parameters
]

# generate and save a boxplot in a file:
def genarate_Boxplot(tableName,data,xTickLabels,yLabel,xLabel):
    plt.rc('font', size=6) # setting figure configuration
    fig = plt.figure()  # creating a new figure
    fig.set_size_inches(8, 6) # setting figure size
    # genarating boxplot
    bp = boxplot(data=data,showmeans=True)
    bp.set(xlabel=xLabel,ylabel=yLabel)
    bp.set_xticklabels(xTickLabels)
    plt.setp(bp.get_xticklabels(), rotation=45)
    plt.savefig('./figs/'+tableName+'.png') # saving figure in a PNG file

# creates a LaTeX formated table and save it on a file:
def generate_Latex_Table(pars,headers,fileName,zipPar=True):
    tabulate.LATEX_ESCAPE_RULES={}
    table = []
    if zipPar:
        l = list(zip_longest(*pars))
    else:
        l = pars
    for i in l:
        table.append(i)
    latexTable = tabulate.tabulate(table, headers=headers, tablefmt='latex')
    with open('dados/'+fileName+'.txt', 'w') as file:
        file.write(latexTable)


for ds in DATA[:1]:
    dsName = ds[0]
    dsData = ds[1]
    X = dsData.data
    y = dsData.target
    # Stage 1:
    names = []
    means = []
    stdevs = []
    for c in CLASSIFIERS[:6]:
        cName = c[0]
        estimator = c[1]()
        scores = []
        # pred = cross_val_predict(estimator,X,y,cv=folds)
        kf = KFold(n_splits=10)
        for train_index, test_index in kf.split(X):
            X_train = [X[i] for i in train_index]
            y_train = [y[i] for i in train_index]
            X_test = [X[i] for i in test_index]
            y_test = [y[i] for i in test_index]
            estimator.fit(X_train,y_train)
            y_pred = estimator.predict(X_test)
            score = accuracy_score(y_test,y_pred)
            scores.append(score)
        names.append(cName)
        means.append(mean(scores))
        stdevs.append(stdev(scores))
    headers = ['Classificador', 'Média das Acurácias', 'DP das Acurácias']
    generate_Latex_Table([names,means,stdevs], headers, 'Fase 1 - '+dsName)


