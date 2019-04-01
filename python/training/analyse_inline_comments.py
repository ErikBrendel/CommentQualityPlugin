import os as os

from joblib import dump

from training.classifier import *
from training.metrics_generation import add_metrics_to_inline_comments
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
                              cache_name_additional='i_train_add', relabel=True):
    frame = read_and_cache_csv(read_cache=should_cache, root_of_repos=data_env,
                               cache_name=cache_name)

    frame = add_metrics_to_inline_comments(frame, read_cache=should_cache,
                                           cache_name=cache_name_additional)

    if relabel:
        frame = relabel_data(frame, class_label, features)
    # show_plot(train_test_frame, y_axis='method_name_length', label=CLASS_LABEL, log_scale_x=False,
    #          remove_outliers=True)
    return frame


if __name__ == '__main__':
    analyse_inline_comments()
