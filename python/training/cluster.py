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


def show_plot(frame: DataFrame, y_axis: str, label: str, x_axis='loc', log_scale_y=True,
              log_scale_x=True, remove_outliers=False):
    plt.figure(figsize=(20, 20))
    if remove_outliers:
        frame = frame.copy()
        frame = frame[frame[x_axis] < frame[x_axis].quantile(.95)]
    alpha = 0.2
    frame['color'] = [[0, 0.8, 0, alpha] if c else [1, 0, 0, alpha] for c in frame[label]]
    frame['x_rnd'] = [1 + x + random.uniform(-0.4, 0.4) for x in frame[x_axis]]
    if y_axis is not 'modifiers':
        frame['y_rnd'] = [1 + x + random.uniform(-0.4, 0.4) for x in frame[y_axis]]
    else:
        frame['y_rnd'] = frame[y_axis]
    if log_scale_x:
        plt.xscale('log')
    if log_scale_y:
        plt.yscale('log')

    plt.scatter(frame['x_rnd'], frame['y_rnd'], c=frame['color'], marker=".")
    plt.title(x_axis + ' ' + y_axis)

    plt.show()


if __name__ == '__main__':
    show_plot(None)
