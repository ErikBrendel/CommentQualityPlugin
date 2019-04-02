"""
Contains a function to load and run a trained classifier on a dataset, to generate a an
evaluation csv-file and print the reasons for the decisions.
"""

import os

from joblib import load

from training.analyse_method_comments import prepare_method_comment_df
from training.training_and_evaluation import print_decisions


def run_method_comment_analysis():
    filename = 'method_comment_pipeline.joblib'
    pipeline = load(filename)
    print(pipeline.steps)
    FEATURES = ['parameterAmount', 'loc', 'tc', 'cc', 'modifiers', 'tocloc', 'annotationNames',
                'methodNameWordCount', 'methodNameLength', 'modifierVisibility']
    SHOULD_CACHE = True
    eval_repo = os.getenv('CSV_ROOT', "../../../CommentRepos/__evaluation")
    eval_frame = prepare_method_comment_df(eval_repo, SHOULD_CACHE, "", FEATURES, relabel=False)

    result = pipeline.predict(eval_frame[FEATURES])
    eval_frame['predicted'] = result
    eval_frame['missing_comment'] = eval_frame.predicted & ~ eval_frame.commented

    missing_comments = eval_frame.loc[eval_frame['missing_comment']]
    print_decisions(pipeline, FEATURES, eval_frame, eval_frame.index.values)
    sum_eval = eval_frame.groupby('filename').sum()
    sum_eval['comment_conformance'] = sum_eval.commented - sum_eval.predicted
    sum_eval.to_csv('complete_result.csv')
    evaluation_result = sum_eval[['loc', 'cc', 'missing_comment']]
    evaluation_result.to_csv('eval_result.csv', sep=';')


if __name__ == '__main__':
    run_method_comment_analysis()
