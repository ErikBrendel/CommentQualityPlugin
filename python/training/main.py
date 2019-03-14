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
    frame = read_and_cache_csv(read_cache=SHOULD_CACHE, repo_root=data_env,
                               cache_name=cache_name_read)
    frame = add_metrics_to_method_comments(frame, read_cache=SHOULD_CACHE,
                                           cache_name=cache_name_additional)
    # Most likely interface methods if no modifier
    frame['modifiers'].fillna("anInterface", inplace=True)
    return frame

def analyse_method_comments():
    REPO_ROOT = os.getenv('CSV_ROOT', "../../../commentMetricsOld")
    EVAL_ROOT = os.getenv('CSV_ROOT', "../../../Evaluation")
    SHOULD_CACHE = True

    train_test_frame = prepare_df(REPO_ROOT, SHOULD_CACHE, 'train_cache', 'train_additional_c')
    eval_frame = prepare_df(EVAL_ROOT, False, 'eval_cache', 'eval_additional_c')

    FEATURES = ['parameterAmount', 'loc', 'tc', 'cc', 'modifiers', 'loctoc',
                'method_name_length', 'method_name_word_count']
    CLASS_LABEL = 'should_comment'

    train_test_frame = relabel_data(train_test_frame, CLASS_LABEL, FEATURES)
    train_test_frame = balance(train_test_frame, CLASS_LABEL)
    #show_plot(train_test_frame, y_axis='method_name_length', label=CLASS_LABEL, log_scale_x=False,
    #          remove_outliers=True)

    train_test_frame['modifiers'] = train_test_frame['modifiers'].astype('category').cat.codes
    labels = train_test_frame[[CLASS_LABEL]]
    X = train_test_frame[FEATURES]

    eval_frame['modifiers'] = eval_frame['modifiers'].astype('category').cat.codes
    eval_X = eval_frame[FEATURES]
    # eventually we should use cross-validation here to prevent overfitting
    x_train, x_test, y_train, y_test = train_test_split(X, labels,
                                                        test_size=0.33,
                                                        random_state=43)

    res = train_and_evaluate([classify_by_dTree, classify_by_randomF, classify_by_extra_tree],
                       x_train,
                       y_train,
                       x_test, y_test, eval_X)

    print(res)
    eval_frame['predicted'] = res[1]
    sum_eval: DataFrame= eval_frame.groupby('filename').sum()
    # quick and dirty hack to prevent zero divisions and make 0/0 be 1 one as it hits the
    # expectation. Todo: Find better way to do this
    #sum_eval.commented += 1
    #sum_eval.predicted += 1
    sum_eval['comment_conformance'] = sum_eval.commented - sum_eval.predicted
    sum_eval.to_csv('complete_result.csv')
    evaluation_result = sum_eval[['loc', 'cc', 'comment_conformance']]
    evaluation_result.to_csv('eval_result.csv')
    # preprocessor = get_preprocessor(x_train)
    # x_train_scaled = preprocessor.transform(x_train)
    # x_test_scaled = preprocessor.transform(
    #     x_test)  # Is not really having an impact for tree-type classifiers
    #
    # train_and_evaluate([classify_by_nn],
    #                    x_train_scaled,
    #                    y_train,
    #                    x_test_scaled, y_test)


if __name__ == '__main__':
    analyse_method_comments()
