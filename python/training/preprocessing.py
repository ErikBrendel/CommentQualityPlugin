from typing import List

from pandas import DataFrame
import pandas as pd
from sklearn import preprocessing
from sklearn.utils import resample


def balance(frame: DataFrame, label: str) -> DataFrame:
    df_majority = frame[frame[label] == False]
    df_minority = frame[frame[label] == True]

    # Upsample minority class
    df_majority_downsampled = resample(df_majority,
                                       replace=False,
                                       n_samples=df_minority.shape[0],
                                       random_state=42)

    # Combine majority class with upsampled minority class
    frame = pd.concat([df_minority, df_majority_downsampled]).sample(frac=1).reset_index(
        drop=True)

    # Display new class counts
    print(frame[label].value_counts())
    return frame


def relabel_data(frame: DataFrame, new_label: str, features: List[str]) -> DataFrame:


    group_by_identical = frame.groupby(features).mean()
    comment_percentag_df = frame.merge(group_by_identical,
                                       on=features,
                                       how='inner', suffixes=('_x', '_percentage'))
    comment_percentag_df[new_label] = comment_percentag_df['commented_percentage'] >= 0.5
    shuffled_frame = comment_percentag_df.sample(frac=1).reset_index(drop=True)

    print("Previously false: ", frame.loc[frame['commented'] == False].shape[0])
    print("Previously true: ", frame.loc[frame['commented'] == True].shape[0])
    now_false_df = shuffled_frame.loc[shuffled_frame[new_label] == False]
    now_true_df = shuffled_frame.loc[shuffled_frame[new_label] == True]
    print("Now False: ", now_false_df.shape[0])
    print("Now True: ", now_true_df.shape[0])
    print("Previously trues that became false ", now_false_df.count().comment)
    print("Previously false that became true ",now_true_df.shape[0] - now_true_df.count().comment)
    print('Pure trues: ', comment_percentag_df.loc[comment_percentag_df['commented_percentage']
                                                   >= 1.0].shape[0])
    print('Pure False: ', comment_percentag_df.loc[comment_percentag_df['commented_percentage']
                                                   <= 0].shape[0])

    return shuffled_frame


def get_preprocessor(x_train: DataFrame):
    scaled = preprocessing.StandardScaler().fit(x_train)
    return scaled
