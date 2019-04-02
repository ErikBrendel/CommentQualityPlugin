import os

from joblib import dump

from training.classifier import *
from training.metrics_generation import add_metrics_to_method_comments
from training.preprocessing import relabel_data
from training.read_data import read_and_cache_csv
from training.training_and_evaluation import train_and_validate_classifiers


def prepare_method_comment_df(data_env, should_cache, class_label, features,
                              cache_name='m_train', cache_name_additional='m_train_add',
                              relabel=True):
    frame = read_and_cache_csv(read_cache=should_cache, root_of_repos=data_env,
                               cache_name=cache_name)

    frame = add_metrics_to_method_comments(frame, read_cache=should_cache,
                                           cache_name=cache_name_additional)

    # Most likely interface methods if no modifier
    frame['modifiers'].fillna("no-modifier", inplace=True)
    frame['annotationNames'].fillna("no-annotation", inplace=True)
    if relabel:
        frame = relabel_data(frame, class_label, features)
    return frame


def analyse_method_comments():
    FEATURES = ['parameterAmount', 'loc', 'tc', 'cc', 'modifiers', 'tocloc', 'annotationNames',
                'methodNameWordCount', 'methodNameLength', 'modifierVisibility']

    FEATURES_TO_ENCODE = ['modifiers', 'annotationNames']
    SHOULD_CACHE = True
    CLASS_LABEL = 'CLASS_LABEL'
    CLASSIFIERS = [StratifiedDummy(), ShortDecisionTree(), DecisionTree(), RandomForest(),
                   ExtraTreeBalanced(), ExtraTree(), KNN()]
    CLASSIFIERS = [RandomForest()]

    training_repos = os.getenv('CSV_ROOT', "../../../CommentRepos/__commentMetrics")
    train_test_frame = prepare_method_comment_df(training_repos, SHOULD_CACHE, CLASS_LABEL,
                                                 FEATURES)

    # for feature in FEATURES:
    #     show_plot('method comments', train_test_frame, y_axis=feature, label=CLASS_LABEL, log_scale_x=False,
    #               log_scale_y=False, jitter=True,
    #               remove_outliers=True)

    pipeline = train_and_validate_classifiers(train_test_frame, FEATURES, FEATURES_TO_ENCODE,
                                              CLASS_LABEL, CLASSIFIERS)

    dump(pipeline, 'method_comment_pipeline.joblib')


if __name__ == '__main__':
    analyse_method_comments()
