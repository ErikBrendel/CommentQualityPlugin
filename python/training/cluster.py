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
    plt.figure(figsize=(12, 12))
    n_samples = 1500
    random_state = 170
    # X, y = make_blobs(n_samples=n_samples, centers=2, random_state=random_state, n_features=10)

    # Incorrect number of clusters
    # y_pred = KMeans(n_clusters=2, random_state=random_state).fit_predict(frame)

    frame['color'] = [[0, 0.6, 0, 0.2] if c else [1, 0, 0, 0.2] for c in frame['commented']]
    # frame['loc_rnd'] = [x + np.random.random(-0.3, 0.3) for x in frame['loc']]

    plt.scatter(frame['loc'], frame['parameterAmount'], c=frame['color'], marker=".")
    # plt.scatter(X_Data.loc[:, 0], X_Data[:, 1], c=y_pred, marker="+")

    plt.title("trololol")

    plt.show()


if __name__ == '__main__':
    cluster(None)
