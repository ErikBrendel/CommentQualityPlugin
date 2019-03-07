import os

from pandas import DataFrame
from sklearn.model_selection import train_test_split

from training.classifier import *
from training.cluster import show_plot
from training.evaluation import performance_report
from training.metrics_generation import add_metrics_to
from training.preprocessing import get_preprocessor, balance, relabel_data
from training.read_data import read_and_cache_csv

if __name__ == '__main__':
    REPO_ROOT = os.getenv('CSV_ROOT', "../commentMetrics")
    SHOULD_CACHE = True
    frame = read_and_cache_csv(read_cache=SHOULD_CACHE, repo_root=REPO_ROOT)
    frame = add_metrics_to(frame, read_cache=SHOULD_CACHE)
    # Most likely interface methods if no modifier
    frame['modifiers'].fillna("anInterface", inplace=True)

    FEATURES = ['parameterAmount', 'loc', 'tc', 'cc', 'modifiers', 'loctoc',
                'method_name_length', 'method_name_word_count']
    CLASS_LABEL = 'should_comment'

    frame = relabel_data(frame, CLASS_LABEL, FEATURES)
    frame = balance(frame, CLASS_LABEL)
    show_plot(frame, y_axis='method_name_length', label=CLASS_LABEL, log_scale_x=False,
              remove_outliers=True)
    frame['modifiers'] = frame['modifiers'].astype('category').cat.codes
    labels = frame[[CLASS_LABEL]]
    X = frame[FEATURES]

    # eventually we should use cross-validation here to prevent overfitting
    x_train, x_test, y_train, y_test = train_test_split(X, labels,
                                                        test_size=0.33,
                                                        random_state=43)

    train_and_evaluate([classify_by_dTree, classify_by_randomF, classify_by_extra_tree],
                       x_train,
                       y_train,
                       x_test, y_test)

    # preprocessor = get_preprocessor(x_train)
    # x_train_scaled = preprocessor.transform(x_train)
    # x_test_scaled = preprocessor.transform(
    #     x_test)  # Is not really having an impact for tree-type classifiers
    #
    # train_and_evaluate([classify_by_nn],
    #                    x_train_scaled,
    #                    y_train,
    #                    x_test_scaled, y_test)
