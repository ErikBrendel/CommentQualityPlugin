from typing import *

import pandas as pd
import numpy as np
from pandas import DataFrame

from sklearn.model_selection import train_test_split
from textblob import TextBlob
from textblob import Word
from textblob.classifiers import DecisionTreeClassifier
from utilities import to_textblob_format, read_and_cache_data, export_csv
import sys
import math
import os

REPO_ROOT = os.getenv('CSV_ROOT', "commentMetrics")
SHOULD_CACHE = True

data_frame = read_and_cache_data(read_cache=SHOULD_CACHE, repo_root=REPO_ROOT)
print(data_frame.count())
comment_and_code_text = data_frame[['commentText', 'codeText']]
comment_and_code_words = data_frame[['commentWords', 'codeWords']]

# export_csv(data_frame)

labels = data_frame[['label']]
x_train, x_test, y_train, y_test = train_test_split(comment_and_code_words, labels,
                                                    test_size=0.33,
                                                    random_state=42)
print('good:', len(labels[labels['label'] == 'good']), 'bad:',
      len(labels[labels['label'] == 'bad']))
train = to_textblob_format(x_train, y_train)
test = to_textblob_format(x_test, y_test)


def to_word_list(word_list: str):
    words = word_list.split(',')
    words = [Word(word).lemmatize() for word in words]
    return words


def basic_metrics(words: List[str]) -> List[int]:
    l = len(words)
    s = set(words)
    ul = len(s)
    return [l, ul, l / ul]


def feature_extractor(word_lists: List[str]):
    [comment, code] = word_lists
    comment_words = to_word_list(comment)
    code_words = to_word_list(code)
    comment_set = set(comment_words)
    code_set = set(code_words)
    set_inters = code_set.intersection(comment_set)

    comment_metrics = basic_metrics(comment_words)
    code_metrics = basic_metrics(code_words)

    return {
        "lengths": comment_metrics[0] / code_metrics[0],
        "uniqueLengths": comment_metrics[1] / code_metrics[1],
        "uniqueness": comment_metrics[2] / code_metrics[2],
        "overlap1": len(set_inters) / len(comment_set),
        "overlap2": len(set_inters) / len(code_set),
    }


dtree_model = DecisionTreeClassifier(train, feature_extractor)
print(dtree_model.pprint())
print(dtree_model.accuracy(test))

# print(train)
