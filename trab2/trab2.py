## -------------------------------------------------------- ##
#   Trab 2 IA 2019-2
#
#   Rafael Belmock Pedruzzi
#
#   Python version: 3.7.4
## -------------------------------------------------------- ##

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

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
from sklearn.metrics import accuracy_score
from seaborn import boxplot
from matplotlib import pyplot as plt
from itertools import zip_longest
import tabulate
from sklearn.model_selection import GridSearchCV, cross_val_score

iris = datasets.load_iris()
digits = datasets.load_digits()
wine = datasets.load_wine()
cancer = datasets.load_breast_cancer()

DATA = [
    # Iris
    ('Iris',          # name
    iris),            # data
    # Digits
    ('Digits',        # name
    digits),          # data
    # Wine
    ('Wine',          # name
    wine),            # data
    # Breast Cancer
    ('Breast Cancer', # name
    cancer)           # data
]

CLASSIFIERS = [
    # 0- ZeroR
    (   'ZeroR',                            # classifier name
        ZeroR,                              # classifier class
        {}),                                # hiperparameters
    # 1- OneR
    (   'OneR',                             # classifier name
        OneR,                               # classifier function
        {}),                                # hiperparameters
    # 2- Probabilistic OneR
    (   'Probabilistic_OneR',               # classifier name
        Prob_OneR,                          # classifier function
        {}),                                # hiperparameters
    # 3- Centroid
    (   'Centroid',                         # classifier name
        Centroid,                           # classifier function
        {}),                                # hiperparameters
    # 4- Centroid OneR
    (   'Centroid_OneR',                    # classifier name
        Centroid_OneR,                      # classifier function
        {}),                                # hiperparameters
    # 5- Gaussian Naive Bayes
    (   'GaussianNB',                       # classifier name
        GaussianNB,                         # classifier class
        {}),                                # hiperparameters
    # 6- Knn
    (   'Knn',                              # classifier name
        KNeighborsClassifier,               # classifier class
        {'n_neighbors':[1, 3, 5, 7, 10]}),  # number of neighbors
    # 7- Decision Tree
    (   'Decision_Tree',                    # classifier name
        DecisionTreeClassifier,             # classifier class
        {'max_depth':[None, 3, 5, 10]}),    # maximum depth
    # 8- Multi-Layer Perceptron
    (   'MLP',                              # classifier name
        MLPClassifier,                      # classifier class
        {'max_iter':[50, 100, 200],         # maximum number of iterations
        'hidden_layer_sizes':[(15,)]}),     # hidden layer sizes
    # 9- Random Forest
    (   'Random_Forest',                    # classifier name
        RandomForestClassifier,             # classifier class
        {'n_estimators':[10, 20, 50, 100]}) # number of estimators
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


for ds in DATA:
    dsName = ds[0] # dataset name
    dsData = ds[1] # dataset data
    X = dsData.data
    y = dsData.target
    # Stage 1
    s1_names = []    # classifiers names
    s1_dsScores = [] # classifiers accuracy
    s1_means = []    # classifiers means
    s1_stdevs = []   # classifiers standard deviation
    for c in CLASSIFIERS[:6]: # from ZeroR to GNB
        cName = c[0]
        estimator = c[1]()
        scores = cross_val_score(estimator, X, y, cv=10)
        s1_names.append(cName)
        s1_dsScores.append(scores)
        s1_means.append(scores.mean())
        s1_stdevs.append(scores.std())
    headers = ['Classificador', 'Média das Acurácias', 'DP das Acurácias']
    generate_Latex_Table([s1_names,s1_means,s1_stdevs], headers, 'Fase 1 - '+dsName)
    genarate_Boxplot('Fase_1_-_'+dsName, s1_dsScores, s1_names, 'Resultados', 'Classificadores')
    # Stage 2
    s2_names = []    # classifiers names
    s2_dsScores = [] # classifiers accuracy
    s2_means = []    # classifiers means
    s2_stdevs = []   # classifiers standard deviation
    for c in CLASSIFIERS[6:]: # from Knn to Random Forest
        cName = c[0]
        estimator = c[1]()
        grid = c[2]
        gs = GridSearchCV(estimator=estimator, param_grid = grid, scoring='accuracy', n_jobs=-1, cv = 4)
        scores = cross_val_score(gs, X, y, scoring='accuracy', cv = 10)
        s2_names.append(cName)
        s2_dsScores.append(scores)
        s2_means.append(scores.mean())
        s2_stdevs.append(scores.std())
    headers = ['Classificador', 'Média das Acurácias', 'DP das Acurácias']
    generate_Latex_Table([s2_names,s2_means,s2_stdevs], headers, 'Fase 2 - '+dsName)
    genarate_Boxplot('Fase_2_-_'+dsName, s2_dsScores, s2_names, 'Resultados', 'Classificadores')
        


