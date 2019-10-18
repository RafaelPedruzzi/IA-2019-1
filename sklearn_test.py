 
import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split, cross_val_score, cross_validate, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix

iris = datasets.load_iris()
x_train, x_test, y_train, y_test = train_test_split(iris.data, iris.target,test_size=0.4, random_state=0)
knn = KNeighborsClassifier()
knn.fit(x_train,y_train)
y_predict = knn.predict(x_test)
knn.score(x_test,y_test)

# confmat=confusion_matrix(y_true=y_test,y_pred=y_predict)

# print("precision score: %.2f" % precision_score(y_pred=y_predict,y_true=y_test,average='macro'))
# print("precision score: %.2f" % precision_score(y_pred=y_predict,y_true=y_test,average='micro'))
# print("precision score: %.2f" % precision_score(y_pred=y_predict,y_true=y_test,average='weighted'))

# print("recall score: %.2f" % recall_score(y_pred=y_predict,y_true=y_test,average='macro'))
# print("recall score: %.2f" % recall_score(y_pred=y_predict,y_true=y_test,average='micro'))
# print("recall score: %.2f" % recall_score(y_pred=y_predict,y_true=y_test,average='weighted'))

# f1_score(y_pred=y_predict,y_true=y_test,average='macro')
# f1_score(y_pred=y_predict,y_true=y_test,average='micro')
# f1_score(y_pred=y_predict,y_true=y_test,average='weighted')

# Kscores = cross_val_score(knn,iris.data,iris.target,cv=5)
# print("Acuracy: %.2f (+/- %0.2f)"%(scores.mean(),scores.std()*2))

# scorings = ['accuracy','precision_macro','recall_macro','f1_macro']
# scores = cross_validate(knn,iris.data,iris.target,scoring=scorings,cv=5)
# scores_acc = scores['test_accuracy']
# print("Acuracy: %.2f (+/- %0.2f)"%(scores_acc.mean(),scores_acc.std()*2))
# scores_prec= scores['test_precision_macro']
# print("Acuracy: %.2f (+/- %0.2f)"%(scores_prec.mean(),scores_prec.std()*2))
# print("Acuracy: %.2f (+/- %0.2f)"%(scores_acc.mean(),scores_acc.std()*2))
# scores_rec= scores['test_recall_macro']
# print("Acuracy: %.2f (+/- %0.2f)"%(scores_rec.mean(),scores_rec.std()*2))
# scores_f1= scores['test_f1_macro']
# print("Acuracy: %.2f (+/- %0.2f)"%(scores_f1.mean(),scores_f1.std()*2))

# grade={'n_neighbors':[1,2,3,4,5,6,7,8,9]}
# gs = GridSearchCV(estimator=knn,param_grid=grade,scoring='accuracy',cv=10)
# gs = gs.fit(x_train,y_train)
# gs.best_score_
# gs.best_params_
# gs.cv_results_.keys()

# grade={'n_neighbors':[1,2,3,4,5,6,7,8,9,10]}
# gs = GridSearchCV(estimator=knn,param_grid=grade,scoring='accuracy',cv=7)
# gs = gs.fit(x_train,y_train)
# gs.best_score_
# 1.0
# gs.cv_results_.keys()


from sklearn import preprocessing

# http://scikit-learn.org/stable/modules/preprocessing.html#scaling-features-to-a-range

max_abs_scaler = preprocessing.MaxAbsScaler()
x_train_maxabs = max_abs_scaler.fit_transform(x_train)
# print("x_train:\n", x_train)
# print("x_train_maxabs:\n", x_train_maxabs)
x_test_maxabs = max_abs_scaler.fit_transform(x_test)
# print("x_test:\n", x_test)
# print("x_test_maxabs:\n", x_test_maxabs)
# print("max_abs_scaler.scale_:\n", max_abs_scaler.scale_)

print("\n######################################\n")

min_max_scaler = preprocessing.MinMaxScaler()
x_train_minmax = min_max_scaler.fit_transform(x_train)
# print("x_train:\n", x_train)
# print("x_train_minmax:\n", x_train_minmax)
x_test_minmax = min_max_scaler.fit_transform(x_test)
# print("x_test:\n", x_test)
# print("x_test_minmax:\n", x_test_minmax)
# print("min_max_scaler.scale_:\n", min_max_scaler.scale_)

min_max_scaler = preprocessing.MinMaxScaler(feature_range=(10,20))
x_train_minmax = min_max_scaler.fit_transform(x_train)
# print("x_train:\n", x_train)
# print("x_train_minmax:\n", x_train_minmax)
x_test_minmax = min_max_scaler.fit_transform(x_test)
# print("x_test:\n", x_test)
# print("x_test_minmax:\n", x_test_minmax)
# print("min_max_scaler.scale_:\n", min_max_scaler.scale_)

x_scaled = preprocessing.scale(x_train)
print("x_scaled:\n", x_scaled)
print("x_scaled.mean:\n", x_scaled.mean(axis=0))
print("x_scaled.std:\n", x_scaled.std(axis=0))

# scaler = 

x_test_scaler = scaler.transform(x_test)
print("x_test:\n", x_test)
print("x_test_scaler:\n", x_test_scaler)
