from pandas import DataFrame
from sklearn import tree
import graphviz
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier


def classify_by_dTree(x_train: DataFrame, y_train: DataFrame, x_test: DataFrame,
                      should_print=True) -> DataFrame:
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
    clf = SGDClassifier(max_iter=1000)
    clf.fit(x_train, y_train.values.ravel())
    predicted = clf.predict(x_test)
    return predicted

def classify_by_randomF(x_train: DataFrame, y_train: DataFrame, x_test: DataFrame) -> DataFrame:
    print('Training Random Forest')
    clf = RandomForestClassifier()
    clf.fit(x_train, y_train.values.ravel())
    return clf.predict(x_test)