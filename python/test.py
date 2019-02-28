from typing import *

import pandas as pd
import numpy as np
from pandas import DataFrame

from sklearn.model_selection import train_test_split
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




# print(train)
