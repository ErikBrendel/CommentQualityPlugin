from statistics import median

import pandas as pd
from sklearn import model_selection
from sklearn.base import ClassifierMixin
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import MultiLabelBinarizer

from training.classifier import *
from training.evaluation import performance_report
from training.preprocessing import balance_train


def train_and_validate_classifiers(train_test_frame: DataFrame, features: List[str],
                                   features_to_encode: List[str], class_label: str,
                                   classifiers: List[ClassifierMixin]) -> Pipeline:
    train_test_frame = train_test_frame.sample(frac=1, random_state=42)  # shuffle all our data!

    labels = train_test_frame[[class_label]]
    X = train_test_frame[features]
    x_train, x_test, y_train, y_test = train_test_split(X, labels,
                                                        test_size=0.33,
                                                        random_state=43)

    scores, best = cross_validate(3, x_train, y_train, 'CLASS_LABEL', features,
                                  features_to_encode, 1, classifiers)
    print(scores)
    print('Best classifier was:', best)
    clf_pipeline = make_pipeline(FeatureEncoder(features_to_encode, features), best())
    clf_pipeline = clf_pipeline.fit(x_train, y_train)
    print_feature_importance(clf_pipeline.steps[0][1].transform(x_train).keys().to_list(),
                             clf_pipeline.steps[1][1])
    predicted = clf_pipeline.predict(x_test)
    performance_report(predicted=predicted, ground_truth=y_test)
    return clf_pipeline


def cross_validate(n, original_x_train, original_y_train, label, features: List[str],
                   features_to_encode: List[str], balance_ratio: float,
                   classifiers: List[ClassifierMixin]):

    X, y = balance_train(original_x_train, original_y_train, label, balance_ratio)
    skf = StratifiedKFold(n_splits=n)
    val_scores = []
    for classifier in classifiers:
        print('Doing ', classifier.__class__)
        clf = make_pipeline(FeatureEncoder(features_to_encode, features), classifier)
        val_scores.append((classifier.__class__, model_selection.cross_validate(clf, X, y,
                                                                                cv=skf, n_jobs=-1)))
    return val_scores, max([(mod, median(res['test_score'])) for mod, res in val_scores],
                           key=lambda x: x[1])[0]


class FeatureEncoder():
    def __init__(self, features_to_encode: List[str], features: List[str]):
        self.features_to_encode = features_to_encode
        self.features = features
        self.encoders = {}
        self.new_feature_names = [f for f in features if f not in features_to_encode]

    def fit(self, df_x: DataFrame, df_y: DataFrame, **fit_params):
        df_x = df_x.copy()
        for feature in self.features_to_encode:
            encoder = MultiLabelBinarizer()
            labels = [x.split(',') for x in list(df_x[feature])]
            encoder.fit(labels)
            new_keys = encoder.classes_
            self.encoders[feature] = encoder
            self.new_feature_names.extend(new_keys)
        return self

    def transform(self, df: DataFrame):
        df = df.copy()
        for feature in self.encoders.keys():
            encoder = self.encoders[feature]
            values = [x.split(',') for x in list(df[feature])]
            new_keys = encoder.classes_
            new_frame = DataFrame(encoder.transform(values), index=df.index, columns=new_keys)
            df = pd.concat([df, new_frame], axis=1, join_axes=[df.index])
            df.drop(feature, axis=1, inplace=True)
        return df


def print_decisions(pipeline: Pipeline, eval_X, eval_frame, indexes):
    encoder = pipeline.steps[0][1]
    classifier = pipeline.steps[1][1]
    if not 'decision_path' in dir(classifier):
        print(classifier, ' Does not support printing decision path')
        return
    eval_X = encoder.transform(eval_X)
    node_indicator = classifier.decision_path(eval_X)
    result = classifier.predict(eval_X)
    for index in indexes:
        if type(classifier) == RandomForest:
            for j, j_tree in enumerate(classifier.estimators_):
                print('Decision Tree: ', j)
                get_decision_path(j_tree, eval_X, eval_frame, node_indicator, result,
                                  index)
        else:
            get_decision_path(classifier, eval_X, eval_frame, node_indicator, result, index)


def get_decision_path(estimator: DecisionTreeClassifier, X_test, eval_frame, node_indicator, result,
                      sample_id):
    leave_id = estimator.apply(X_test)
    feature = estimator.tree_.feature
    threshold = estimator.tree_.threshold

    node_index = node_indicator.indices[node_indicator.indptr[sample_id]:
                                        node_indicator.indptr[sample_id + 1]]
    print('\n')
    print(eval_frame.iloc[sample_id])
    print('Rules used to predict sample id:', sample_id)
    print('\n')
    for node_id in node_index:
        if leave_id[sample_id] == node_id:
            continue

        if (X_test.iloc[sample_id, feature[node_id]] <= threshold[node_id]):
            threshold_sign = "<="
        else:
            threshold_sign = ">"

        print("decision id node %s : (X_test[%s, %s] (= %s) %s %s)"
              % (node_id,
                 sample_id,
                 X_test.keys()[feature[node_id]],
                 X_test.iloc[sample_id, feature[node_id]],
                 threshold_sign,
                 threshold[node_id]
                 ))
    print('predicted %s' % result[sample_id])


