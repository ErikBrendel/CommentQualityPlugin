import pandas as pd
import numpy as np
from pandas import DataFrame, Series
from sklearn.linear_model import SGDClassifier

from sklearn.model_selection import train_test_split
from utilities import to_textblob_format, read_and_cache_data, export_csv
import os
import scipy.sparse as sp
from sklearn import metrics
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

REPO_ROOT = os.getenv('CSV_ROOT', "commentMetrics")
SHOULD_CACHE = True

data_frame = read_and_cache_data(read_cache=SHOULD_CACHE, repo_root=REPO_ROOT)
data_frame['allWords'] = [x + "," + y for key, [x, y] in data_frame[['commentWords', 'codeWords']].iterrows()]

print(data_frame.count())
comment_and_code_text = data_frame[['commentText', 'codeText']]
comment_and_code_words = data_frame[['commentWords', 'codeWords', 'allWords']]

# export_csv(data_frame)

labels = data_frame[['label']]
x_train, x_test, y_train, y_test = train_test_split(comment_and_code_words, labels,
                                                    test_size=0.33,
                                                    random_state=42)
print('good:', len(labels[labels['label'] == 'good']), 'bad:',
      len(labels[labels['label'] == 'bad']))
#train = to_textblob_format(x_train, y_train)
#test = to_textblob_format(x_test, y_test)


# print(train)

text_preprocess = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer())
])

text_preprocess.fit(x_train['allWords'])


def merge(comment, code):
    a = text_preprocess.transform(comment)
    b = text_preprocess.transform(code)
    return sp.hstack((a, b, a.multiply(b), (a - b).power(2)))


x_train_idf = merge(x_train['commentWords'], x_train['codeWords'])
x_test_idf = merge(x_test['commentWords'], x_test['codeWords'])

clf = SGDClassifier(loss='hinge', penalty='l2',
                    alpha=1e-3, random_state=42,
                    max_iter=500, tol=None)

clf.fit(x_train_idf, y_train.values.ravel())
predicted = clf.predict(x_test_idf)
#print(predicted)
print(metrics.classification_report(y_test, predicted))
print(metrics.confusion_matrix(y_test, predicted))
