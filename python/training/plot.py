import random

import matplotlib.pyplot as plt
from pandas import DataFrame

from training.preprocessing import balance


def show_plot(title: str, frame: DataFrame, y_axis: str, label: str, x_axis='loc', log_scale_y=True,
              log_scale_x=True, remove_outliers=False, jitter=True, should_balance=False):
    """
    Plots any two features plus the class as color as a scatter plot

    :param title: Name of the plot
    :param frame: data to plot
    :param y_axis: feature name for y-axis
    :param label: name of class label
    :param x_axis: feature name of x-axis
    :param log_scale_y: use log scale for y-axis
    :param log_scale_x: use log scale for x-axis
    :param remove_outliers: remove anything that is not below the 95-percentile
    :param jitter: Slightly move each dot for better visibility
    :param should_balance: Equalize amount of items for each class
    :return:
    """

    frame = frame.copy()
    plt.figure(dpi=400)
    # frame = frame.sample(frac=0.5, random_state=42)
    font = {'family': 'DejaVu Sans',
            'size': 8}
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.rc('font', **font)
    plt.title(title + ': ' + x_axis + " - " + y_axis)
    if should_balance:
        frame = balance(frame, label, 1)

    if remove_outliers:
        frame = frame.copy()
        frame = frame[frame[x_axis] < frame[x_axis].quantile(.95)]
    alpha = 0.2
    frame['color'] = [[0, 0.8, 0, alpha] if c else [1, 0, 0, alpha] for c in frame[label]]
    if jitter:
        # Add some space between the points
        frame['x_rnd'] = [1 + x + random.uniform(-0.4, 0.4) for x in frame[x_axis]]
        if y_axis not in ['modifiers', 'annotationNames', 'type']:
            frame['y_rnd'] = [1 + x + random.uniform(-0.4, 0.4) for x in frame[y_axis]]
        else:
            frame['y_rnd'] = frame[y_axis]
    else:
        frame['x_rnd'] = frame[x_axis]
        frame['y_rnd'] = frame[y_axis]
    if log_scale_x:
        plt.xscale('log')
    if log_scale_y:
        plt.yscale('log')

    plt.scatter(frame['x_rnd'], frame['y_rnd'], c=frame['color'], edgecolors='none',
                marker='.')

    plt.show()
    plt.close()
