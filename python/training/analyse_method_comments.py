import os

from training.metrics_generation import add_metrics_to_method_comments
from training.read_data import read_and_cache_csv
from training.training_and_evaluation import train_for, evaluate_repo_with


def prepare_method_comment_df(data_env, SHOULD_CACHE, cache_name, cache_name_additional):
    frame = read_and_cache_csv(read_cache=SHOULD_CACHE, root_of_repos=data_env,
                               cache_name=cache_name)
    frame = add_metrics_to_method_comments(frame, read_cache=SHOULD_CACHE,
                                           cache_name=cache_name_additional)
    # Most likely interface methods if no modifier
    frame['modifiers'].fillna("no-modifier", inplace=True)
    frame['annotationNames'].fillna("", inplace=True)
    return frame


def analyse_method_comments():
    # FEATURES = ['parameterAmount', 'loc', 'tc', 'cc', 'modifiers', 'tocloc',
    #             'method_name_length', 'method_name_word_count']
    FEATURES = ['parameterAmount', 'loc', 'tc', 'cc', 'modifiers', 'tocloc', 'annotationNames',
                'methodNameWordCount', 'methodNameLength', 'modifierVisibility']
    # FEATURES = ['parameterAmount', 'loc', 'modifiers', 'annotations', 'methodNameWordCount', 'methodNameLength']
    FEATURES_TO_ENCODE = ['modifiers', 'annotationNames']
    SHOULD_CACHE = True

    training_repos = os.getenv('CSV_ROOT', "../../../CommentRepos/__commentMetrics")
    train_test_frame = prepare_method_comment_df(training_repos, SHOULD_CACHE, 'm_train', 'm_train_add')
    models, encoders = train_for(train_test_frame, FEATURES, FEATURES_TO_ENCODE)

    # generating software quality metrics:
    # repo_path = '../../../OneEval'
    # eval_frame = prepare_method_comment_df(repo_path, SHOULD_CACHE, 'm_eval', 'm_eval_add')
    # evaluate_repo_with(eval_frame, models[0], FEATURES, encoders)


if __name__ == '__main__':
    analyse_method_comments()
