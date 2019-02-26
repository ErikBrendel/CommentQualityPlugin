import pandas as pd
import glob
import os
import sys
from textblob import TextBlob
from textblob.classifiers import DecisionTreeClassifier

REPO_ROOT =  "commentMetrics"

metrics_files = os.path.join(REPO_ROOT, "**", "*.csv")

for filename in glob.iglob(metrics_files, recursive=True):
    data = pd.read_csv(filename, sep=';').rename(columns={"# id": "id"})
    data['survivalAmount'] = 1
    data2 = data.groupby(["id", "commentWords", "codeWords"]).agg({"survivalAmount": pd.np.sum})
    data2.to_csv(sys.stdout)
    print(filename)
    break
