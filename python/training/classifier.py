from pandas import DataFrame
from sklearn import tree
import graphviz
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier
from typing import List, Callable

from training.evaluation import performance_report


def classify_by_dTree(x_train: DataFrame, y_train: DataFrame, x_test: DataFrame,
                      should_print=False) -> DataFrame:
    print('Training dTree')
    clf = tree.DecisionTreeClassifier()
    clf.fit(x_train, y_train)
    predicted = clf.predict(x_test)
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
    clf = RandomForestClassifier()
    clf.fit(x_train, y_train.values.ravel())
    return clf.predict(x_test)


def train_and_evaluate(classifiers: List[Callable[[DataFrame, DataFrame, DataFrame], DataFrame]],
                       x_train: DataFrame, y_train: DataFrame, x_test: DataFrame,
                       y_test: DataFrame):
    for func in classifiers:
        predicted = func(x_train, y_train, x_test)
        performance_report(y_test, predicted)
