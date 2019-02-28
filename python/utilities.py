from typing import Tuple, List
from pandas import DataFrame
import glob
import os
import sys
import pandas as pd
from pandas import DataFrame
import difflib
from math import log10 as log
from math import inf as INFINITY


def to_textblob_format(x: DataFrame, y: DataFrame) -> List[Tuple[str, str]]:
    texts = []
    for _, x_row in x.iterrows():
        comment = x_row[0]
        code = x_row[1]
        text_line = [comment, code]
        texts.append(text_line)
    labels = []
    for _, y_row in y.iterrows():
        label = y_row[0]
        labels.append(label)
    result = []
    for text, label in zip(texts, labels):
        result.append((text, label))

    return result


def read_and_cache_data(number_of_items=INFINITY, *, repo_root, read_cache) -> DataFrame:
    metrics_files = os.path.join(repo_root, "**", "*.csv")
    comment_frame = None
    comment_list = []

    for filename in glob.iglob(metrics_files, recursive=True):
        if os.path.isfile('cache') and read_cache:
            comment_frame = pd.read_pickle('cache')
            break
        if len(comment_list) > number_of_items:
            break
        print(filename)
        df = pd.read_csv(filename, sep=';').rename(columns={"# id": "id"})
        df.fillna('', inplace=True)

        # needed until pandas 24.2: https://github.com/pandas-dev/pandas/issues/25406
        df['id'] = df['id'].apply(lambda cid: "_" + cid)

        # data.to_csv(sys.stdout, sep=";")
        comment_ids = df["id"].unique()
        for comment_id in comment_ids:
            versions_data = df.loc[df["id"] == comment_id]

            old_comment_words = versions_data.iloc[0]['commentWords']
            old_code_words = versions_data.iloc[0]['codeWords']
            old_comment_text = versions_data.iloc[0]['commentText']
            old_code_text = versions_data.iloc[0]['codeText']
            old_timestamp = versions_data.iloc[0]['timestamp']

            for key, row_data in versions_data.iloc[1:].iterrows():
                if row_data['commentWords'] != old_comment_words and row_data['codeWords'] == old_code_words \
                        and are_reasonably_different(row_data['commentWords'], old_comment_words):
                    comment_list.append({
                        'id': comment_id,
                        'timestamp': old_timestamp,
                        'commentWords': old_comment_words,
                        'codeWords': old_code_words,
                        'commentText': old_comment_text,
                        'codeText': old_code_text,
                        'label': 'bad'})
                    if len(comment_list) >= 2 and comment_list[-2]['id'] == comment_list[-1]['id']:
                        comment_list.pop(-2)
                    comment_list.append({
                        'id': comment_id,
                        'timestamp': row_data['timestamp'],
                        'commentWords': row_data['commentWords'],
                        'codeWords': old_code_words,
                        'commentText': row_data['commentText'],
                        'codeText': old_code_text,
                        'label': 'good'})

                old_comment_words = row_data['commentWords']
                old_code_words = row_data['codeWords']
                old_comment_text = row_data['commentText']
                old_code_text = row_data['codeText']
                old_timestamp = row_data['timestamp']

    print()
    print()

    cols = ['id', 'timestamp', 'label', 'commentWords', 'codeWords', 'commentText', 'codeText']
    comment_frame = comment_frame if comment_frame is not None else pd.DataFrame(comment_list,
                                                                                 columns=cols)

    if comment_frame.count == 0:
        print("No data found, exiting...")
        sys.exit(0)

    comment_frame.to_pickle('cache')
    return comment_frame


def are_reasonably_different(s1: str, s2: str) -> bool:
    ratio = difflib.SequenceMatcher(None, s1, s2).quick_ratio()
    return ratio < 0.85


def export_csv(data_frame: DataFrame):
    data_frame['code_length'] = [log(len(x.split(','))) for x in data_frame['codeWords']]
    data_frame['comment_length'] = [log(len(x.split(','))) for x in data_frame['commentWords']]
    data_frame['code_set'] = [set(x.split(',')) for x in data_frame['codeWords']]
    data_frame['comment_set'] = [set(x.split(',')) for x in data_frame['commentWords']]

    data_frame['code_length_unique'] = [log(len(x)) for x in data_frame['code_set']]
    data_frame['comment_length_unique'] = [log(len(x)) for x in data_frame['comment_set']]
    data_frame['code_uniqueness'] = data_frame['code_length_unique'] / data_frame['code_length']
    data_frame['comment_uniqueness'] = data_frame['comment_length_unique'] / data_frame['comment_length']

    data_frame['intersection_set_length'] = [len(x.intersection(y)) for key, [x, y] in
                                             data_frame[['code_set', 'comment_set']].iterrows()]

    data_frame['lengths'] = data_frame['comment_length'] / data_frame['code_length']
    data_frame['uniqueLengths'] = data_frame['comment_length_unique'] / data_frame['code_length_unique']
    data_frame['uniqueness'] = data_frame['comment_uniqueness'] / data_frame['code_uniqueness']
    data_frame['overlap1'] = data_frame['intersection_set_length'] / data_frame['code_length_unique']
    data_frame['overlap2'] = data_frame['intersection_set_length'] / data_frame['comment_length_unique']

    data_frame[['label', 'lengths', 'uniqueLengths', 'uniqueness', 'overlap1', 'overlap2']].to_csv("out.csv", sep=';')
    sys.exit(0)