"""
Contains the function to analyse inline comments, generate and persist a classifier
"""

import os as os

from joblib import dump

from training.classifier import *
from training.metrics_generation import add_metrics_to_inline_comments
from training.plot import show_plot
from training.preprocessing import relabel_data
from training.read_data import read_and_cache_csv
from training.training_and_evaluation import train_and_validate_classifiers


def analyse_inline_comments():
    training_repos = os.getenv('CSV_ROOT', "../../../CommentRepos/__commentLineMetrics")
    SHOULD_CACHE = True
    FEATURES = ['loc', 'conditionChildren', 'condition_length', 'nloc', 'cc', 'tc', 'type',
                'containingMethodHasComment', 'containedComments']

    FEATURES_TO_ENCODE = ['type']
    CLASS_LABEL = 'CLASS_LABEL'
    CLASSIFIERS = [StratifiedDummy(), ShortDecisionTree(), DecisionTree(), RandomForest(),
                   ExtraTreeBalanced(), ExtraTree(), KNN()]

    train_test_frame = prepare_inline_comment_df(training_repos, SHOULD_CACHE,
                                                 CLASS_LABEL, FEATURES)

    pipeline = train_and_validate_classifiers(train_test_frame, FEATURES, FEATURES_TO_ENCODE,
                                              CLASS_LABEL, CLASSIFIERS)

    dump(pipeline, 'inline_comment_pipeline.joblib')


def prepare_inline_comment_df(data_env, should_cache, class_label, features, cache_name='i_train',
                              cache_name_additional='i_train_add', relabel=True,
                              visualize_features=False):
    frame = read_and_cache_csv(read_cache=should_cache, root_of_repos=data_env,
                               cache_name=cache_name)

    frame = add_metrics_to_inline_comments(frame, read_cache=should_cache,
                                           cache_name=cache_name_additional)

    if relabel:
        frame = relabel_data(frame, class_label, features)

    if visualize_features:
        for feature in features:
            show_plot('inline comments', frame, y_axis=feature, label=class_label,
                      log_scale_x=False,
                      log_scale_y=False, jitter=True, remove_outliers=True, should_balance=True)
    return frame


if __name__ == '__main__':
    analyse_inline_comments()
