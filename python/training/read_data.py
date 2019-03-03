import os
from pandas import DataFrame
import glob
import os
import sys
import pandas as pd
from pandas import DataFrame
import difflib
from math import log10 as log
from math import inf as INFINITY


def read_and_cache_csv(number_of_items=INFINITY, *, repo_root, read_cache) -> DataFrame:
    metrics_files = os.path.join(repo_root, "**", "*.csv")
    if os.path.isfile('frame_cache') and read_cache:
        df = pd.read_pickle('frame_cache')
        return df
    df_list = []
    for filename in glob.iglob(metrics_files, recursive=True):
        if 'test' in filename:
            continue
        print(filename)
        df_list.append(pd.read_csv(filename, sep=';'))
    df = pd.concat(df_list, ignore_index=True)
    df.to_pickle('frame_cache')
    print('done')
    return df
