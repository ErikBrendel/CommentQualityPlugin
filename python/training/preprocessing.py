from typing import List

from pandas import DataFrame
import pandas as pd
from sklearn import preprocessing
from sklearn.utils import resample


def balance(frame: DataFrame, label: str) -> DataFrame:
    df_majority = frame[frame[label] == False]
    df_minority = frame[frame[label] == True]

    df_majority_downsampled = resample(df_majority,
                                       replace=False,
                                       n_samples=df_minority.shape[0],
                                       random_state=42)

    frame = pd.concat([df_minority, df_majority_downsampled]).sample(frac=1).reset_index(drop=True)

    # Display new class counts
    print(frame[label].value_counts())
    return frame


def balance_train(x_train, y_train, label: str, amount: float):
    df_majority = x_train[y_train[label] == False]
    df_minority = x_train[y_train[label] == True]
    dfy_majority = y_train[y_train[label] == False]
    dfy_minority = y_train[y_train[label] == True]

    target_amount = int(df_minority.shape[0] + (1.0 - amount) * (df_majority.shape[0] - df_minority.shape[0]))
    df_majority_downsampled = resample(df_majority, replace=False,
                                       n_samples=target_amount, random_state=42)
    dfy_majority_downsampled = resample(dfy_majority, replace=False,
                                        n_samples=target_amount, random_state=42)

    x_train = pd.concat([df_minority, df_majority_downsampled]).sample(frac=1).reset_index(drop=True)
    y_train = pd.concat([dfy_minority, dfy_majority_downsampled]).sample(frac=1).reset_index(drop=True)

    # Display new class counts
    print("balanced by amount " + str(amount))
    print(y_train[label].value_counts())
    return x_train, y_train


def relabel_data(frame: DataFrame, new_label: str, features: List[str]) -> DataFrame:


    group_by_identical = frame.groupby(features).mean()
    comment_percentage_df = frame.merge(group_by_identical,
                                       on=features,
                                       how='inner', suffixes=('_x', '_percentage'))
    comment_percentage_df[new_label] = comment_percentage_df['commented_percentage'] >= 0.5
    shuffled_frame = comment_percentage_df.sample(frac=1).reset_index(drop=True)

    print("Previously false: ", frame.loc[frame['commented'] == False].shape[0])
    print("Previously true: ", frame.loc[frame['commented'] == True].shape[0])
    now_false_df = shuffled_frame.loc[shuffled_frame[new_label] == False]
    now_true_df = shuffled_frame.loc[shuffled_frame[new_label] == True]
    print("Now False: ", now_false_df.shape[0])
    print("Now True: ", now_true_df.shape[0])
    print("Previously trues that became false ", now_false_df.count().comment)
    print("Previously false that became true ",now_true_df.shape[0] - now_true_df.count().comment)
    print('Pure trues: ', comment_percentage_df.loc[comment_percentage_df['commented_percentage']
                                                   >= 1.0].shape[0])
    print('Pure False: ', comment_percentage_df.loc[comment_percentage_df['commented_percentage']
                                                   <= 0].shape[0])

    return shuffled_frame


def get_preprocessor(x_train: DataFrame):
    scaled = preprocessing.StandardScaler().fit(x_train)
    return scaled
