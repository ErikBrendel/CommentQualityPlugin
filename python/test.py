import pandas as pd
import glob
import os
import sys

REPO_ROOT =  "commentMetrics"

metrics_files = os.path.join(REPO_ROOT, "**", "*.csv")

for filename in glob.iglob(metrics_files, recursive=True):
    data = pd.read_csv(filename, sep=';').rename(columns={"# id": "id"}).set_index(
        ['id', 'timestamp'])
    data.to_csv(sys.stdout)
    print(filename)
