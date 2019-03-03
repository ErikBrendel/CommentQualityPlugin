import os

from pandas import DataFrame

from training.cluster import cluster
from training.metrics_generation import add_metrics_to
from training.read_data import read_and_cache_csv

if __name__ == '__main__':
    REPO_ROOT = os.getenv('CSV_ROOT', "../commentMetrics")
    SHOULD_CACHE = True
    frame = read_and_cache_csv(read_cache=SHOULD_CACHE, repo_root=REPO_ROOT)
    frame = add_metrics_to(frame)
    cluster(frame)

