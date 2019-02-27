import pandas as pd
import glob
import os
import sys
from textblob import TextBlob
from textblob.classifiers import DecisionTreeClassifier

REPO_ROOT = "commentMetrics"
SHOULD_CACHE = True
metrics_files = os.path.join(REPO_ROOT, "**", "*.csv")
comment_frame = None
comment_list = []

for filename in glob.iglob(metrics_files, recursive=True):
    if os.path.isfile('cache') and SHOULD_CACHE:
        comment_frame = pd.read_pickle('cache')
        break
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
                comment_list.append({
                    'id': comment_id,
                    'timestamp': old_timestamp,
                    'commentWords': old_comment,
                    'codeWords': old_code,
                    'commentText': old_comment_text,
                    'codeText': old_code_text,
                    'label': 'bad'})
                if len(comment_list) >= 2 and comment_list[-2]['id'] == comment_list[-1]['id']:
                    comment_list.pop(-2)
                comment_list.append({
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
comment_frame = comment_frame if comment_frame is not None else pd.DataFrame(comment_list,
                                                                          columns=cols)
comment_frame.to_pickle('cache')
data = comment_frame[['commentWords', 'codeWords', 'label']]

data.to_csv(sys.stdout, sep=';')
