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


def read_and_cache_csv(number_of_items=INFINITY, *, cache_name, repo_root, read_cache) -> DataFrame:
    metrics_files = os.path.join(repo_root, "**", "*.csv")
    if os.path.isfile(cache_name) and read_cache:
        df = pd.read_pickle(cache_name)
        print('Cache: read date from cache', cache_name)
        return df
    df_list = []
    for filename in glob.iglob(metrics_files, recursive=True):
        if '/test/' in filename:
            continue
        print(filename)
        new_frame = pd.read_csv(filename, sep=';')
        new_frame['filename'] = filename[len(repo_root)+1:-4]
        df_list.append(new_frame)
    df = pd.concat(df_list, ignore_index=True)
    df.to_pickle(cache_name)
    print('Updated Cache ', cache_name)
    return df
