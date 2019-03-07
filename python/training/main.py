import os

from pandas import DataFrame
from sklearn.model_selection import train_test_split

from training.classifier import *
from training.cluster import show_plot
from training.evaluation import performance_report
from training.metrics_generation import add_metrics_to
from training.preprocessing import get_preprocessor, balance
from training.read_data import read_and_cache_csv

if __name__ == '__main__':
    REPO_ROOT = os.getenv('CSV_ROOT', "../commentMetrics")
    SHOULD_CACHE = True
    frame = read_and_cache_csv(read_cache=SHOULD_CACHE, repo_root=REPO_ROOT)
    frame = add_metrics_to(frame, read_cache=SHOULD_CACHE)
    frame['modifiers'].fillna("constructorOrInterface", inplace=True) # No modifier is likely a
    group = frame.groupby(['parameterAmount', 'loc', 'tc', 'cc',  'modifiers']).mean()
    frame_2 = frame.merge(group, on=['parameterAmount', 'loc', 'tc', 'cc', 'modifiers'],
                how='inner', suffixes=('_x','_percentage'))
    frame_3 = frame_2.sample(frac=1).reset_index(drop=True)
    frame_3['new_cls'] = frame_3['commented_percentage'] >= 0.5

    # constructor or an Interface
    # frame = balance(frame)
    #show_plot(frame, y_axis='modifiers')
    #frame = frame.drop_duplicates(['parameterAmount', 'loc', 'tc', 'cc',  'modifiers'])
    frame['modifiers'] = frame['modifiers'].astype('category').cat.codes

    frame['loctoc'] = frame['loc']/frame['tc']

    labels = frame[['commented']]
    X = frame[['parameterAmount', 'loc', 'tc', 'cc',  'modifiers', 'loctoc']]

    # eventually we should use cross-validation here to prevent overfitting
    x_train, x_test, y_train, y_test = train_test_split(X, labels,
                                                        test_size=0.33,
                                                        random_state=43)



    train_and_evaluate([classify_by_dTree, classify_by_randomF, classify_by_extra_tree],
                       x_train,
                       y_train,
                       x_test, y_test)

    preprocessor = get_preprocessor(x_train)
    x_train_scaled = preprocessor.transform(x_train)
    x_test_scaled = preprocessor.transform(x_test) # Is not really having an impact for tree-type classifiers

    train_and_evaluate([ classify_by_nn],
                       x_train_scaled,
                       y_train,
                       x_test_scaled, y_test)

