import os as os
from training.metrics_generation import add_metrics_to_inline_comments
from training.read_data import read_and_cache_csv
from training.training_and_evaluation import train_for, evaluate_repo_with


def analyse_inline_comments():
    training_repos = os.getenv('CSV_ROOT', "../../../CommentRepos/__commentLineMetrics")
    SHOULD_CACHE = True
    FEATURES = [
        'loc', 'conditionChildren', 'condition_length', 'nloc', 'cc', 'tc', 'type',
        'containingMethodHasComment', 'containedComments'
    ]
    FEATURES_TO_ENCODE = ['type']
    train_test_frame = prepare_inline_comment_df(training_repos, SHOULD_CACHE, 'i_train', 'i_train_add')
    models, encoders = train_for(train_test_frame, FEATURES, FEATURES_TO_ENCODE)

    # generating software quality metrics:
    # eval_repo = '../../../OneEvalLine'
    # eval_frame = prepare_inline_comment_df(eval_repo, SHOULD_CACHE, 'i_eval', 'i_eval_add')
    # evaluate_repo_with(eval_frame, models[0], FEATURES, encoders)


def prepare_inline_comment_df(data_env, SHOULD_CACHE, cache_name, cache_name_additional):
    frame = read_and_cache_csv(read_cache=SHOULD_CACHE, root_of_repos=data_env,
                               cache_name=cache_name)
    frame = add_metrics_to_inline_comments(frame, read_cache=SHOULD_CACHE,
                                           cache_name=cache_name_additional)
    return frame


if __name__ == '__main__':
    analyse_inline_comments()
