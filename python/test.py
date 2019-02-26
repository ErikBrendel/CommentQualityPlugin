import pandas as pd
import glob
import os
import sys
from textblob import TextBlob
from textblob.classifiers import DecisionTreeClassifier

REPO_ROOT = "commentMetrics"

metrics_files = os.path.join(REPO_ROOT, "**", "*.csv")

result = []

for filename in glob.iglob(metrics_files, recursive=True):
    df = pd.read_csv(filename, sep=';').rename(columns={"# id": "id"})
    # data.to_csv(sys.stdout, sep=";")
    comment_ids = df["id"].unique()
    for comment_id in comment_ids:
        versions_data = df.loc[df["id"] == comment_id]

        old_comment = versions_data.iloc[0]['commentWords']
        old_code = versions_data.iloc[0]['codeWords']
        old_timestamp = versions_data.iloc[0]['timestamp']
        for key, row_data in versions_data.iloc[1:].iterrows():
            if row_data['commentWords'] != old_comment and row_data['codeWords'] == old_code:
                result.append({
                    'id': comment_id,
                    'timestamp': old_timestamp,
                    'commentWords': old_comment,
                    'codeWords': old_code,
                    'label': 'bad'})
                result.append({
                    'id': comment_id,
                    'timestamp': row_data['timestamp'],
                    'commentWords': row_data['commentWords'],
                    'codeWords': old_code,
                    'label': 'good'})

            old_comment = row_data['commentWords']
            old_code = row_data['codeWords']
    print(filename)

print()
print()

result = pd.DataFrame(result, columns=['id', 'timestamp', 'commentWords', 'codeWords', 'label'])
result.to_csv(sys.stdout, sep=';')
