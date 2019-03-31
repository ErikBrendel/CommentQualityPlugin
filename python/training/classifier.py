import copy

from pandas import DataFrame
from sklearn import tree
import graphviz as graphviz
from sklearn.base import ClassifierMixin
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.ensemble.forest import ForestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree._tree import TREE_LEAF
from typing import List, Callable

from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier

from training.evaluation import performance_report

def prune(tree):
    tree = copy.deepcopy(tree)
    dat = tree.tree_
    nodes = range(0, dat.node_count)
    ls = dat.children_left
    rs = dat.children_right
    classes = [[list(e).index(max(e)) for e in v] for v in dat.value]

    leaves = [(ls[i] == rs[i]) for i in nodes]

    LEAF = -1
    for i in reversed(nodes):
        if leaves[i]:
            continue
        if leaves[ls[i]] and leaves[rs[i]] and classes[ls[i]] == classes[rs[i]]:
            ls[i] = rs[i] = LEAF
            leaves[i] = True
    return tree


def print_feature_importance(x_train: DataFrame, clf: ForestClassifier):
    print(list(zip(x_train.keys().to_list(), map(lambda x: round(x * 100, 3),
                                                 clf.feature_importances_))))

def classify_by_dTree(x_train: DataFrame, y_train: DataFrame, should_print=False):
    print('Training dTree')
    clf = tree.DecisionTreeClassifier(class_weight='balanced',min_samples_leaf=10)
    clf.fit(x_train, y_train)
    # clf = prune(clf)
    print_feature_importance(x_train, clf)
    if should_print:
        dot_data = tree.export_graphviz(clf, feature_names=x_train.keys().values, class_names=['no', 'comment'],
                                        out_file=None, rounded=True, filled=True)
        graph = graphviz.Source(dot_data)
        graph.render("dtree")
    return clf


def classify_by_short_dTree(x_train: DataFrame, y_train: DataFrame, should_print=True):
    print('Training short 5 depth dTree')
    clf = tree.DecisionTreeClassifier(class_weight='balanced',max_depth=5, min_samples_leaf=100)
    clf.fit(x_train, y_train)
    # clf = prune(clf)
    print_feature_importance(x_train, clf)
    if should_print:
        dot_data = tree.export_graphviz(clf, feature_names=x_train.keys().values, class_names=['no', 'comment'],
                                        out_file=None, rounded=True, filled=True)
        graph = graphviz.Source(dot_data)
        graph.render("short_tree")
    return clf


def classify_by_SGD(x_train: DataFrame, y_train: DataFrame):
    print('Training SGD')
    # Really bad for some reason
    clf = SGDClassifier(max_iter=1000)
    clf.fit(x_train, y_train.values.ravel())
    return clf


def classify_by_randomF(x_train: DataFrame, y_train: DataFrame):
    print('Training Random Forest')
    clf = RandomForestClassifier(n_estimators=10)
    clf.fit(x_train, y_train.values.ravel())
    print_feature_importance(x_train, clf)
    return clf


def classify_by_extra_tree_balanced(x_train: DataFrame, y_train: DataFrame):
    print('Training Balancing Extra Tree')
    clf = ExtraTreesClassifier(class_weight='balanced',n_estimators=100)
    clf.fit(x_train, y_train.values.ravel())
    print_feature_importance(x_train, clf)
    return clf

def classify_by_extra_tree(x_train: DataFrame, y_train: DataFrame):
    print('Training Extra Tree')
    clf = ExtraTreesClassifier(n_estimators=100)
    clf.fit(x_train, y_train.values.ravel())
    print_feature_importance(x_train, clf)
    return clf

class ExtraTree(ExtraTreesClassifier):
    def __init__(self):
        super().__init__(n_estimators=100, n_jobs=-1)
        self.name = 'Extra Tree'

    def fit(self, x_train, y_train):
        return super().fit(x_train, y_train.values.ravel())

class ExtraTreeBalanced(ExtraTreesClassifier):
    def __init__(self):
        super().__init__(class_weight='balanced',n_estimators=100, n_jobs=-1)
        self.name = 'Extra Tree Balanced'

    def fit(self, x_train, y_train):
        return super().fit(x_train, y_train.values.ravel())

class RandomForest(RandomForestClassifier):
    def __init__(self):
        super().__init__(n_estimators=100,n_jobs=-1)
        self.name = "Random Forest"

    def fit(self, x_train, y_train):
        return super().fit(x_train, y_train.values.ravel())

class ShortDecisionTree(DecisionTreeClassifier):
    def __init__(self):
        super().__init__(class_weight='balanced',max_depth=5, min_samples_leaf=100)
        self.name = 'Short Decision Tree'


class StratifiedDummy(DummyClassifier):
    def __init__(self):
        super().__init__(random_state=42)

    def fit(self, X, y, sample_weight=None):
        return super().fit(X, y.should_comment.to_numpy(), sample_weight=None)


class DecisionTree(DecisionTreeClassifier):
    def __init__(self):
        super().__init__(min_samples_leaf=100)
        self.name = 'Decision Tree'

    def fit(self, x_train, y_train, **kwargs):
        self.features = x_train.keys().values
        return super().fit(x_train,y_train,**kwargs)

    def print_tree(self, x_train):
        dot_data = tree.export_graphviz(self, feature_names=x_train.keys().values,
                                        class_names=['no', 'comment'],
                                        out_file=None, rounded=True, filled=True)
        graph = graphviz.Source(dot_data)
        graph.render("short_tree")


class KNN(KNeighborsClassifier):
    def fit(self, x_train, y_train):
        return super().fit(x_train, y_train.values.ravel())


def classify_by_knn(x_train: DataFrame, y_train: DataFrame):
    print('Training Knn')
    clf = KNeighborsClassifier()
    clf.fit(x_train, y_train.values.ravel())
    return clf


def classify_by_nn(x_train: DataFrame, y_train: DataFrame):
    print('Training NN')
    clf = MLPClassifier(alpha=1e-5,
                        hidden_layer_sizes=(100, 100, 10), random_state=42, max_iter=1000)
    clf.fit(x_train, y_train.values.ravel())
    return clf

def classify_by_dummy(x_train: DataFrame, y_train: DataFrame):
    print('Training Dummy classifier')
    clf = DummyClassifier(random_state=42)
    clf.fit(x_train, y_train.should_comment.to_numpy())
    return clf



def train_models(
        classifiers: List[Callable[[DataFrame, DataFrame, DataFrame], ForestClassifier]],
        x_train: DataFrame, y_train: DataFrame) -> List[ForestClassifier]:
    """Potentially returns something other than a Forest Classifier, but this is useful for type
    annotations"""
    trained_models = []
    for func in classifiers:
        print('\n')
        classifier = func(x_train, y_train)
        trained_models.append(classifier)
    return trained_models

def train_and_evaluate(
        classifiers: List[Callable[[DataFrame, DataFrame, DataFrame], ForestClassifier]],
        x_train: DataFrame, y_train: DataFrame, x_test: DataFrame,
        y_test: DataFrame) -> List[ForestClassifier]:
    """Potentially returns something other than a Forest Classifier, but this is useful for type
    annotations"""
    trained_models = []
    for func in classifiers:
        print('\n')
        classifier = func(x_train, y_train)
        predicted = classifier.predict(x_test)
        trained_models.append(classifier)
        performance_report(predicted=predicted, ground_truth=y_test)
    return trained_models
