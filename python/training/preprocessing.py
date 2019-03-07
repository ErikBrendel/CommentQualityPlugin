from pandas import DataFrame
import pandas as pd
from sklearn import preprocessing
from sklearn.utils import resample

def balance(frame: DataFrame, label: str)-> DataFrame:
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

def encode_labels(frame:DataFrame):
    pass

def get_preprocessor(x_train: DataFrame):

    scaled = preprocessing.StandardScaler().fit(x_train)
    return scaled
