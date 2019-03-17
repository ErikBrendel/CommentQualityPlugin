from typing import Tuple, Dict

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier

from training.classifier import *
from training.preprocessing import balance, relabel_data


def train_for(train_test_frame: DataFrame, features: List[str], features_to_encode: List[str]) \
        -> Tuple[List[ForestClassifier], Dict[str, LabelEncoder]]:
    CLASS_LABEL = 'should_comment'

    train_test_frame = relabel_data(train_test_frame, CLASS_LABEL, features)
    train_test_frame = balance(train_test_frame, CLASS_LABEL)
    # show_plot(train_test_frame, y_axis='method_name_length', label=CLASS_LABEL, log_scale_x=False,
    #          remove_outliers=True)

    labels = train_test_frame[[CLASS_LABEL]]
    X = train_test_frame[features]
    # eventually we should use cross-validation here to prevent overfitting
    x_train, x_test, y_train, y_test = train_test_split(X, labels,
                                                        test_size=0.33,
                                                        random_state=43)
    encoders, x_train = create_encoder_and_encode(x_train, features_to_encode)
    x_test = encode_frame_with(encoders, x_test)

    models = train_and_evaluate([classify_by_short_dTree, classify_by_dTree, classify_by_randomF,
                                 classify_by_extra_tree, classify_by_knn],
                                x_train,
                                y_train,
                                x_test, y_test)

    return models, encoders


def create_encoder_and_encode(df: DataFrame, features_to_encode: List[str]) \
        -> Tuple[Dict[str, LabelEncoder], DataFrame]:
    encoders = {}
    df = df.copy()
    for feature in features_to_encode:
        encoder = LabelEncoder()
        labels = list(set(df[feature])) + ['<unknown>']
        encoder.fit(labels)
        df[feature] = encoder.transform(df[feature])
        encoders[feature] = encoder
    return encoders, df


def encode_frame_with(encoders: Dict[str, LabelEncoder], df: DataFrame) -> DataFrame:
    df = df.copy()
    for feature in encoders.keys():
        encoder = encoders[feature]
        df[feature] = [val if val in encoder.classes_ else '<unknown>' for val in df[feature]]
        df[feature] = encoder.transform(df[feature])
    return df


def evaluate_repo_with(eval_frame, classifier, features: List[str], encoders: Dict[str,
                                                                                   LabelEncoder]):
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