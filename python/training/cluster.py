import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame

from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs


def cluster(frame: DataFrame):
    plt.figure(figsize=(12, 12))

    n_samples = 1500
    random_state = 170
    X, y = make_blobs(n_samples=n_samples, centers=2, random_state=random_state, n_features=10)

    # Incorrect number of clusters
    y_pred = KMeans(n_clusters=2, random_state=random_state).fit_predict(X)

    plt.scatter(X[:, 0], X[:, 1], c=y_pred)

    plt.title("Incorrect Number of Blobs")

    plt.show()