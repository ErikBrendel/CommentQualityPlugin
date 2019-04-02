"""
Contains classifier classes which inherit from scikit classifiers learn and mostly just contain
some convenience functionality to make instantiation and training more easy to use.
"""

import copy
from typing import List

import graphviz as graphviz
from sklearn import tree
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.ensemble.forest import ForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier


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


def print_feature_importance(keys: List[str], clf: ForestClassifier):
    print(len(clf.feature_importances_))
    print(list(zip(keys, map(lambda x: round(x * 100, 3), clf.feature_importances_))))



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
        return super().fit(X, y.CLASS_LABEL.to_numpy(), sample_weight=None)


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


class NeuralNetwork(MLPClassifier):
    def __init__(self):
        self._scaler = None
        super().__init__(alpha=1e-5, hidden_layer_sizes=(100, 100, 10),
                         random_state=42, max_iter=1000)

    def fit(self, X, y):
        self._scaler = StandardScaler().fit(X)
        x_train = self._scaler.transform(X)
        return super().fit(x_train, y.values.ravel())

    def predict(self, X):
        return super().predict(self._scaler.transform(X))


class KNN(KNeighborsClassifier):
    def fit(self, x_train, y_train):
        return super().fit(x_train, y_train.values.ravel())


