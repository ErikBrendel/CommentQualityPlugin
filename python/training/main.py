import os

from pandas import DataFrame
from sklearn.model_selection import train_test_split

from training.classifier import classify_by_dTree, classify_by_SGD, classify_by_randomF, \
    train_and_evaluate
from training.cluster import show_plot
from training.evaluation import performance_report
from training.metrics_generation import add_metrics_to
from training.preprocessing import get_preprocessor, balance
from training.read_data import read_and_cache_csv

if __name__ == '__main__':
    REPO_ROOT = os.getenv('CSV_ROOT', "../commentMetrics")
    SHOULD_CACHE = True
    frame = read_and_cache_csv(read_cache=SHOULD_CACHE, repo_root=REPO_ROOT)
    frame = add_metrics_to(frame)
    cluster(frame)

