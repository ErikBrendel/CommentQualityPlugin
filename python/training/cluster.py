import random

import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame

from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn import preprocessing


def normalize(df):
    result = df.copy()
    for feature_name in df.columns:
        max_value = df[feature_name].max()
        min_value = df[feature_name].min()
        result[feature_name] = (df[feature_name] - min_value) / (max_value - min_value)
    return result


def cluster(frame: DataFrame):
    plt.figure(figsize=(20, 20))
    n_samples = 1500
    random_state = 170
    # X, y = make_blobs(n_samples=n_samples, centers=2, random_state=random_state, n_features=10)

    # Incorrect number of clusters
    # y_pred = KMeans(n_clusters=2, random_state=random_state).fit_predict(frame)

    alpha = 0.2
    frame['color'] = [[0, 0.8, 0, alpha] if c else [1, 0, 0, alpha] for c in frame['commented']]
    frame['parameterAmount_rnd'] = [1 + x + random.uniform(-0.4, 0.4) for x in frame['parameterAmount']]
    frame['loc_rnd'] = [1 + x + random.uniform(-0.4, 0.4) for x in frame['loc']]

    frame = frame.sample(frac=1).reset_index(drop=True)

    plt.xscale('log')
    plt.yscale('log')
    plt.scatter(frame['loc_rnd'], frame['parameterAmount_rnd'], c=frame['color'], marker=".")
    # plt.scatter(X_Data.loc[:, 0], X_Data[:, 1], c=y_pred, marker="+")

    plt.title("trololol")

    plt.show()


if __name__ == '__main__':
    cluster(None)
