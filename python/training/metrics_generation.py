import os
import pandas as pd

import lizard
from pandas import DataFrame

from training.cluster import show_plot


def add_metrics_to(frame: DataFrame, *, read_cache) -> DataFrame:
    """modifies dataframe in place"""
    if os.path.isfile('additional_metrics_cache') and read_cache:
        cached_frame = pd.read_pickle('additional_metrics_cache')
        print('CACHE: Read metrics from cache')
        return cached_frame
    frame['cc'] = frame.apply(
        lambda row: lizard.analyze_file.analyze_source_code(
            "placeholder.java",
            row['code']).CCN,
        axis=1)
    frame['tc'] = frame.apply(
        lambda row: lizard.analyze_file.analyze_source_code(
            "placeholder.java",
            row['code']).token_count,
        axis=1)
    frame.to_pickle('additional_metrics_cache')
    print('done adding metrics')
    return frame


if __name__ == '__main__':
    l = lizard.analyze_file.analyze_source_code("placeholder.java",
                                                'private int doneAreYou(int i){\nreturn 4\n}')
    l2 = lizard.analyze_file.analyze_source_code("placeholder.java",
                                                '/**\n*This is a a comment\n*@param int '
                                                'done mach dings\n*/\nprivate int '
                                                'doneAreYou(int '
                                                'i){'
                                                '\n\treturn 4\n}')

    frame = DataFrame({'code': ['public void do(){}', 'private int done(int i){return 4}',
                                'private int indent(int i){\nif(i>10)\n\treturn '
                                '4\nelse\n\treturn3}']})


