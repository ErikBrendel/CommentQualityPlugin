from typing import Tuple, Dict

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer
from sklearn.tree import DecisionTreeClassifier

from training.classifier import *
from training.preprocessing import balance, relabel_data, balance_train


def flat_list(list_of_lists):
    return [item for sublist in list_of_lists for item in sublist]


def train_for(train_test_frame: DataFrame, features: List[str], features_to_encode: List[str]) \
        -> Tuple[List[ForestClassifier], Dict[str, MultiLabelBinarizer]]:
    CLASS_LABEL = 'should_comment'

    train_test_frame = relabel_data(train_test_frame, CLASS_LABEL, features)
    # train_test_frame = balance(train_test_frame, CLASS_LABEL)
    # show_plot(train_test_frame, y_axis='method_name_length', label=CLASS_LABEL, log_scale_x=False,
    #          remove_outliers=True)

    train_test_frame = train_test_frame.sample(frac=1, random_state=42)  # shuffle all our data!

    labels = train_test_frame[[CLASS_LABEL]]
    X = train_test_frame[features]
    # eventually we should use cross-validation here to prevent overfitting
    x_train, x_test, y_train, y_test = train_test_split(X, labels,
                                                        test_size=0.33,
                                                        random_state=43)

    x_train, y_train = balance_train(x_train, y_train, CLASS_LABEL, 0)

    encoders, x_train, features = create_encoder_and_encode(x_train, features_to_encode, features)
    x_test = encode_frame_with(encoders, x_test)

    models = train_and_evaluate([classify_by_short_dTree, classify_by_dTree,
                                 classify_by_randomF, classify_by_extra_tree],
                                x_train,
                                y_train,
                                x_test, y_test)

    return models, encoders


def create_encoder_and_encode(df: DataFrame, features_to_encode: List[str], features: List[str]) \
        -> Tuple[Dict[str, MultiLabelBinarizer], DataFrame, List[str]]:
    encoders = {}
    new_feature_names = [f for f in features if f not in features_to_encode]
    df = df.copy()
    for feature in features_to_encode:
        encoder = MultiLabelBinarizer()
        labels = [x.split(',') for x in list(df[feature])]
        encoder.fit(labels)
        new_keys = encoder.classes_
        new_frame = DataFrame(encoder.transform(labels), index=df.index, columns=new_keys)
        df = pd.concat([df, new_frame], axis=1, join_axes=[df.index])
        encoders[feature] = encoder
        new_feature_names.extend(new_keys)
        df.drop(feature, axis=1, inplace=True)
    return encoders, df, new_feature_names


def encode_frame_with(encoders: Dict[str, MultiLabelBinarizer], df: DataFrame) -> DataFrame:
    df = df.copy()
    for feature in encoders.keys():
        encoder = encoders[feature]
        values = [x.split(',') for x in list(df[feature])]
        new_keys = encoder.classes_
        new_frame = DataFrame(encoder.transform(values), index=df.index, columns=new_keys)
        df = pd.concat([df, new_frame], axis=1, join_axes=[df.index])
        df.drop(feature, axis=1, inplace=True)
    return df


def evaluate_repo_with(eval_frame, classifier, features: List[str], encoders: Dict[str,
                                                                                   MultiLabelBinarizer]):
    eval_X = eval_frame[features]
    eval_X = encode_frame_with(encoders, eval_X)
    result = classifier.predict(eval_X)
    eval_frame['predicted'] = result
    eval_frame['missing_comment'] = eval_frame.predicted & ~ eval_frame.commented

    missing_comments = eval_frame.loc[eval_frame['missing_comment']]
    print_decisions(classifier, eval_X, eval_frame, missing_comments.index.values)
    sum_eval = eval_frame.groupby('filename').sum()
    sum_eval['comment_conformance'] = sum_eval.commented - sum_eval.predicted
    sum_eval.to_csv('complete_result.csv')
    evaluation_result = sum_eval[['loc', 'cc', 'missing_comment']]
    evaluation_result.to_csv('eval_result.csv')


def print_decisions(classifier: DecisionTreeClassifier, eval_X, eval_frame, indexes):
    node_indicator = classifier.decision_path(eval_X)
    result = classifier.predict(eval_X)
    leave_id = classifier.apply(eval_X)
    for index in indexes:
        get_decision_path(classifier, eval_X, eval_frame, node_indicator, result, leave_id, index)


def get_decision_path(estimator: DecisionTreeClassifier, X_test, eval_frame, node_indicator, result,
                      leave_id, sample_id):
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
