import os

from pandas import DataFrame
from sklearn.model_selection import train_test_split

from training.classifier import *
from training.cluster import show_plot
from training.evaluation import performance_report
from training.metrics_generation import add_metrics_to_method_comments
from training.preprocessing import get_preprocessor, balance, relabel_data
from training.read_data import read_and_cache_csv


def prepare_df(data_env, SHOULD_CACHE, cache_name_read, cache_name_additional):
    frame = read_and_cache_csv(read_cache=SHOULD_CACHE, root_of_repos=data_env,
                               cache_name=cache_name_read)
    frame = add_metrics_to_method_comments(frame, read_cache=SHOULD_CACHE,
                                           cache_name=cache_name_additional)
    # Most likely interface methods if no modifier
    frame['modifiers'].fillna("anInterface", inplace=True)
    frame['modifiers_text'] = frame['modifiers']
    frame['modifiers'] = frame['modifiers'].astype('category').cat.codes
    frame['annotations_text'] = frame['annotations']
    frame['annotations'] = frame['annotations'].astype('category').cat.codes
    return frame


def train_for_method_comments(use_cache: bool, training_repos: str, features: List[str]):
    train_test_frame = prepare_df(training_repos, use_cache, 'train_cache', 'train_additional_c')
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

    models = train_and_evaluate([classify_by_dTree, classify_by_randomF, classify_by_extra_tree],
                                x_train,
                                y_train,
                                x_test, y_test)

    return models

    # preprocessor = get_preprocessor(x_train)
    # x_train_scaled = preprocessor.transform(x_train)
    # x_test_scaled = preprocessor.transform(
    #     x_test)  # Is not really having an impact for tree-type classifiers
    #
    # train_and_evaluate([classify_by_nn],
    #                    x_train_scaled,
    #                    y_train,
    #                    x_test_scaled, y_test)


def evaluate_repo_with(classifier, repo_path:str,  use_cache: bool, features):
    eval_frame = prepare_df(repo_path, use_cache, 'eval_cache', 'eval_additional_c')
    eval_X = eval_frame[features]
    result = classifier.predict(eval_X)
    eval_frame['predicted'] = result
    eval_frame['missing_comment'] = eval_frame.predicted & ~ eval_frame.commented

    sum_eval: DataFrame = eval_frame.groupby('filename').sum()
    sum_eval['comment_conformance'] = sum_eval.commented - sum_eval.predicted
    sum_eval.to_csv('complete_result.csv')
    evaluation_result = sum_eval[['loc', 'cc', 'missing_comment']]
    evaluation_result.to_csv('eval_result.csv')


def main():
    # FEATURES = ['parameterAmount', 'loc', 'tc', 'cc', 'modifiers', 'loctoc',
    #             'method_name_length', 'method_name_word_count']
    FEATURES = ['parameterAmount', 'loc', 'tc', 'cc', 'modifiers', 'loctoc', 'annotations',
                'methodNameWordCount','methodNameLength', 'nrInlineComments']
    SHOULD_CACHE = False

    training_repos = os.getenv('CSV_ROOT', "../../../CommentRepos/__commentMetrics")
    models = train_for_method_comments(SHOULD_CACHE, training_repos, FEATURES)

    #repo_path = os.getenv('CSV_ROOT', "../../../NewVersion")
    #evaluate_repo_with(models[1], repo_path, SHOULD_CACHE, FEATURES)

if __name__ == '__main__':
   main()

