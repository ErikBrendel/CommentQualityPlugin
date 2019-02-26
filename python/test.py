import pandas as pd
import glob
import os
import sys

REPO_ROOT = "/home/erik/Documents/repos/qualityCommentRepos/"

for file in os.listdir(REPO_ROOT):
    metrics_files = os.path.join(REPO_ROOT, file, "commentMetrics", "**", "*.csv")

    for filename in glob.iglob(metrics_files, recursive=True):
        data = pd.read_csv(filename, sep=';').rename(columns={"# id": "id"}).set_index(['id', 'timestamp'])
        data.to_csv(sys.stdout)
        print(filename)
