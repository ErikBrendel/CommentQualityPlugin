import pandas as pd
from pandas import DataFrame

from sklearn.model_selection import train_test_split
from textblob import TextBlob
from textblob.classifiers import DecisionTreeClassifier
from utilities import to_textblob_format, read_and_cache_data

REPO_ROOT = "commentMetrics"
SHOULD_CACHE = False

data_frame = read_and_cache_data(read_cache=SHOULD_CACHE, repo_root=REPO_ROOT)
print(data_frame.count())
comment_and_code_text = data_frame[['commentText', 'codeText']]
comment_and_code_words = data_frame[['commentWords', 'codeWords']]

labels = data_frame[['label']]
x_train, x_test, y_train, y_test = train_test_split(comment_and_code_text, labels,
                                                    test_size=0.33,
                                                    random_state=42)
print('good:', len(labels[labels['label'] == 'good']), 'bad:',
      len(labels[labels['label'] == 'bad']))
train = to_textblob_format(x_train, y_train)
test = to_textblob_format(x_test, y_test)


def feature_extractor(text: str):
    comment, code = text.split(' |||| ')
    comment_lemmas= TextBlob(comment).split().lemmatize()
    return {}


dtree_model = DecisionTreeClassifier(train)
print(dtree_model.pprint())
print(dtree_model.accuracy(test))

# print(train)
