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


def show_plot(frame: DataFrame, y_axis: str, x_axis='loc', log_scale_y=False):
    plt.figure(figsize=(20, 20))

    alpha = 0.2
    frame['color'] = [[0, 0.8, 0, alpha] if c else [1, 0, 0, alpha] for c in frame['commented']]
    frame['x_rnd'] = [1 + x + random.uniform(-0.4, 0.4) for x in frame[x_axis]]
    frame['y_rnd'] = [1 + x + random.uniform(-0.4, 0.4) for x in frame[y_axis]]


    #frame = frame.sample(frac=1).reset_index(drop=True)
    plt.xscale('log')
    if log_scale_y:
        plt.yscale('log')

    plt.scatter(frame['x_rnd'], frame['y_rnd'], c=frame['color'], marker=".")
    plt.title(x_axis + ' ' + y_axis)


    plt.show()


if __name__ == '__main__':
    show_plot(None)
