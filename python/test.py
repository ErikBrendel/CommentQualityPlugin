import pandas as pd
import numpy as np
from pandas import DataFrame, Series
from sklearn.linear_model import SGDClassifier

from sklearn.model_selection import train_test_split
from utilities import to_textblob_format, read_and_cache_data, export_csv
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
#train = to_textblob_format(x_train, y_train)
#test = to_textblob_format(x_test, y_test)


# print(train)
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
text_clf = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', SGDClassifier(loss='hinge', penalty='l2',
                          alpha=1e-3, random_state=42,
                          max_iter=5, tol=None)),
])
text_clf.fit(x_train['commentWords'], y_train.values.ravel())
predicted = text_clf.predict(x_test['commentWords'])
#print(predicted)
from sklearn import metrics
print(metrics.classification_report(y_test, predicted))
print(metrics.confusion_matrix(y_test, predicted))
