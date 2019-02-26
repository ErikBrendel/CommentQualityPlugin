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
    df.fillna('', inplace=True)
    # data.to_csv(sys.stdout, sep=";")
    comment_ids = df["id"].unique()
    for comment_id in comment_ids:
        versions_data = df.loc[df["id"] == comment_id]

        old_comment = versions_data.iloc[0]['commentWords']
        old_code = versions_data.iloc[0]['codeWords']
        old_comment_text = versions_data.iloc[0]['commentText']
        old_code_text = versions_data.iloc[0]['codeText']
        old_timestamp = versions_data.iloc[0]['timestamp']
        for key, row_data in versions_data.iloc[1:].iterrows():
            if row_data['commentWords'] != old_comment and row_data['codeWords'] == old_code \
                    and abs(len(row_data['commentWords']) - len(old_comment)) > 3:
                result.append({
                    'id': comment_id,
                    'timestamp': old_timestamp,
                    'commentWords': old_comment,
                    'codeWords': old_code,
                    'commentText': old_comment_text,
                    'codeText': old_code_text,
                    'label': 'bad'})
                if len(result) >= 2 and result[-2]['id'] == result[-1]['id']:
                    result.pop(-2)
                result.append({
                    'id': comment_id,
                    'timestamp': row_data['timestamp'],
                    'commentWords': row_data['commentWords'],
                    'codeWords': old_code,
                    'commentText': row_data['commentText'],
                    'codeText': old_code_text,
                    'label': 'good'})

            old_comment = row_data['commentWords']
            old_code = row_data['codeWords']
            old_comment_text = row_data['commentText']
            old_code_text = row_data['codeText']
            old_timestamp = row_data['timestamp']
    print(filename)

print()
print()

cols = ['id', 'timestamp', 'label', 'commentWords', 'codeWords', 'commentText', 'codeText']
result = pd.DataFrame(result, columns=cols)
result.to_csv(sys.stdout, sep=';')
