import os
from multiprocessing.pool import Pool

from pandas import DataFrame
import glob
import os
import sys
import pandas as pd
from pandas import DataFrame
import difflib
from math import log10 as log
from math import inf as INFINITY


def read_and_cache_csv(*, cache_name, root_of_repos,
                       read_cache) -> DataFrame:
    filename_offset = len(root_of_repos) + 1
    if os.path.isfile(cache_name) and read_cache:
        df = pd.read_pickle(cache_name)
        print('Cache: read date from cache', cache_name)
        return df

    repo_list = [(root_of_repos, repo) for repo in os.listdir(root_of_repos) if os.path.isdir(
        root_of_repos + '/' + repo)]
    with Pool() as p:
        df_list = p.map(read_repo, repo_list)
    if len(df_list) > 1:
        df = pd.concat(df_list, ignore_index=True)
    else:
        df = df_list[0]
    df.to_pickle(cache_name)
    print('Updated Cache ', cache_name)
    return df


def read_repo(repo_root) -> DataFrame:
    repo_path = repo_root[0] + '/' + repo_root[1]
    df_list = []
    metrics_files = os.path.join(repo_path, "**", "*.csv")
    for filename in glob.iglob(metrics_files, recursive=True):
        if '/test/' in filename:
            continue
        print(filename)
        new_frame = pd.read_csv(filename, sep=';')
        new_frame['filename'] = filename[filename.find(repo_root[1]):-4]
        df_list.append(new_frame)
    if len(df_list) > 1:
        repo_df = pd.concat(df_list, ignore_index=True)
        return repo_df
    else:
        return df_list[0]
