from pandas import DataFrame
from sklearn import tree
import graphviz
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.linear_model import SGDClassifier
from typing import List, Callable

from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier

from training.evaluation import performance_report


def classify_by_dTree(x_train: DataFrame, y_train: DataFrame, x_test: DataFrame,
                      should_print=True) -> DataFrame:
    print('Training dTree')
    clf = tree.DecisionTreeClassifier()
    clf.fit(x_train, y_train)
    predicted = clf.predict(x_test)
    print(x_train.keys().to_list())
    print(clf.feature_importances_)
    if should_print:
        dot_data = tree.export_graphviz(clf, out_file=None)
        graph = graphviz.Source(dot_data)
        graph.render("iris")
    return predicted


def classify_by_SGD(x_train: DataFrame, y_train: DataFrame, x_test: DataFrame) -> DataFrame:
    print('Training SGD')
    # Really bad for some reason
    clf = SGDClassifier(max_iter=1000)
    clf.fit(x_train, y_train.values.ravel())
    predicted = clf.predict(x_test)
    return predicted


def classify_by_randomF(x_train: DataFrame, y_train: DataFrame, x_test: DataFrame) -> DataFrame:
    print('Training Random Forest')
    clf = RandomForestClassifier(n_estimators=10)
    clf.fit(x_train, y_train.values.ravel())
    print(x_train.keys().to_list())
    print(clf.feature_importances_)
    return clf.predict(x_test)


def classify_by_extra_tree(x_train: DataFrame, y_train: DataFrame, x_test: DataFrame) -> DataFrame:
    print('Training Extra Tree')
    clf = ExtraTreesClassifier(n_estimators=10)
    clf.fit(x_train, y_train.values.ravel())
    print(x_train.keys().to_list())
    print(clf.feature_importances_)
    return clf.predict(x_test)


def classify_by_knn(x_train: DataFrame, y_train: DataFrame, x_test: DataFrame) -> DataFrame:
    print('Training Knn')
    clf = KNeighborsClassifier()
    clf.fit(x_train, y_train.values.ravel())
    return clf.predict(x_test)


def classify_by_nn(x_train: DataFrame, y_train: DataFrame, x_test: DataFrame) -> DataFrame:
    print('Training NN')
    clf = MLPClassifier(alpha=1e-5,
                        hidden_layer_sizes=(100, 100, 10), random_state=42, max_iter=1000)
    clf.fit(x_train, y_train.values.ravel())
    return clf.predict(x_test)


def train_and_evaluate(classifiers: List[Callable[[DataFrame, DataFrame, DataFrame], DataFrame]],
                       x_train: DataFrame, y_train: DataFrame, x_test: DataFrame,
                       y_test: DataFrame):
    for func in classifiers:
        predicted = func(x_train, y_train, x_test)
        performance_report(predicted=predicted, ground_truth=y_test)
