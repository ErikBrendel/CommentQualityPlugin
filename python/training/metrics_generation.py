import datetime
import os
import pandas as pd

import lizard
from pandas import DataFrame


def create_cache_dir(cache_name):
    cache_name = 'caches/' + cache_name
    os.makedirs('caches', exist_ok=True)
    return cache_name


def add_metrics_to_inline_comments(frame: DataFrame, *, read_cache, cache_name) -> DataFrame:
    cache_name = create_cache_dir(cache_name)
    start = datetime.datetime.now()
    if os.path.isfile(cache_name) and read_cache:
        cached_frame = pd.read_pickle(cache_name)
        print('CACHE: Read metrics from cache ', cache_name)
        return cached_frame
    frame['lizard'] = [lizard.analyze_file.analyze_source_code("pl.java", code) for code in
                       frame['code']]
    frame['cc'] = [l.CCN for l in frame['lizard']]
    frame['tc'] = [l.token_count for l in frame['lizard']]
    frame['nloc'] = [l.nloc for l in frame['lizard']]

    frame.drop('lizard', axis=1, inplace=True)
    frame.to_pickle(cache_name)
    print('done adding metrics. Stored in cache: ', cache_name)
    end = datetime.datetime.now()
    print('took', end - start)
    return frame


def add_metrics_to_method_comments(frame: DataFrame, *, read_cache, cache_name) -> DataFrame:
    """modifies dataframe in place"""
    cache_name = create_cache_dir(cache_name)
    if os.path.isfile(cache_name) and read_cache:
        cached_frame = pd.read_pickle(cache_name)
        print('CACHE: Read metrics from cache ', cache_name)
        return cached_frame

    frame['lizard'] = [lizard.analyze_file.analyze_source_code("pl.java", code) for code in
                       frame['code']]
    frame['cc'] = [l.CCN for l in frame['lizard']]
    frame['tc'] = [l.token_count for l in frame['lizard']]


    # frame['method_name'] = [l.function_list[0].name if len(l.function_list) > 0 else "" for l in frame['lizard']]
    # frame['method_name_length'] = [len(name) for name in frame['method_name']]
    # frame['method_name_word_count'] = [sum(1 for c in name if c.isupper()) for name in frame['method_name']]

    frame.drop('lizard', axis=1, inplace=True)

    frame['tocloc'] = frame['tc'] / frame['loc']

    frame.to_pickle(cache_name)
    print('done adding metrics. Stored in cache: ', cache_name)
    return frame


if __name__ == '__main__':
    l = lizard.analyze_file.analyze_source_code("placeholder.java",
                                                'public int doneAreYou(int i)')
    l2 = lizard.analyze_file.analyze_source_code("placeholder.java",
                                                 '/**\n*This is a a comment\n*@param int '
                                                 'done mach dings\n*/\nprivate int '
                                                 'doneAreYou(int '
                                                 'i){'
                                                 '\n\treturn 4\n}')
    l3 = lizard.analyze_file.analyze_source_code("placeholder.java", """// Explicit reference equality is added here just in case Arrays.equals does not have one
if (primaryConstructorArgTypes == argumentTypes || Arrays.equals(primaryConstructorArgTypes, argumentTypes)) {
    // This skips "get constructors" machinery
    return ReflectUtils.newInstance(primaryConstructor, arguments);
}""")

    frame = DataFrame({'code': ['public void do(){}', 'private int done(int i){return 4}',
                                'private int indent(int i){\nif(i>10)\n\treturn '
                                '4\nelse\n\treturn3}']})
