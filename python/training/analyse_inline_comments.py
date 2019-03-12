import os

from pandas import DataFrame
from sklearn.model_selection import train_test_split

from training.classifier import *
from training.cluster import show_plot
from training.evaluation import performance_report
from training.metrics_generation import add_metrics_to_inline_comments
from training.preprocessing import get_preprocessor, balance, relabel_data
from training.read_data import read_and_cache_csv

def analyse_inline_comments():
    REPO_ROOT = os.getenv('CSV_ROOT', "../../../qualityCommentRepos/__commentMetrics")
    SHOULD_CACHE = True
    frame = read_and_cache_csv(read_cache=SHOULD_CACHE, repo_root=REPO_ROOT,
                               cache_name='inline_frame_cache')
    frame = add_metrics_to_inline_comments(frame, read_cache=SHOULD_CACHE, cache_name='inline_metrics_cache')

    FEATURES = ['loc', 'conditionChildren', 'condition_length']
    CLASS_LABEL = 'commented'

    frame = relabel_data(frame, CLASS_LABEL, FEATURES)
    #frame = balance(frame, CLASS_LABEL)
    show_plot(frame, y_axis='condition_length', label=CLASS_LABEL,
              remove_outliers=False)
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

if __name__ == '__main__':
    analyse_inline_comments()