from pandas import DataFrame
from sklearn import metrics


def performance_report(predicted: DataFrame, ground_truth: DataFrame):
    print(metrics.classification_report(ground_truth, predicted, target_names=['no comment',
                                                                               'comment']))
    print('Actual class\nno_comment|comment')
    print(metrics.confusion_matrix(ground_truth, predicted))
