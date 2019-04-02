import glob
import os
from multiprocessing.pool import Pool

import pandas as pd
from pandas import DataFrame

from training.metrics_generation import create_cache_dir


def read_and_cache_csv(*, cache_name, root_of_repos, read_cache) -> DataFrame:
    cache_name = create_cache_dir(cache_name)

    if os.path.isfile(cache_name) and read_cache:
        df = pd.read_pickle(cache_name)
        print('Cache: read date from cache', cache_name)
        return df

    repo_list = [(root_of_repos, repo) for repo in os.listdir(root_of_repos) if os.path.isdir(
        root_of_repos + '/' + repo)]
    with Pool() as p:
        df_list = p.map(_read_repo, repo_list)
    if len(df_list) > 1:
        df = pd.concat(df_list, ignore_index=True, sort=False)
    else:
        df = df_list[0]

    if read_cache:
        df.to_pickle(cache_name)
        print('Updated Cache ', cache_name)
    return df


def _read_repo(repo_root) -> DataFrame:
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
        repo_df = pd.concat(df_list, ignore_index=True, sort=False)
        return repo_df
    else:
        if not df_list:
            print('no files to evaluate in repo')
            exit()
        return df_list[0]
