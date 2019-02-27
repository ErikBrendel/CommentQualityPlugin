from typing import Tuple, List
from pandas import DataFrame


def to_textblob_format(x: DataFrame, y: DataFrame) -> List[Tuple[str, str]]:
    texts = []
    for _, x_row in x.iterrows():
        comment = x_row[0]
        code = x_row[1]
        text_line = comment + ' |||| ' + code
        texts.append(text_line)
    labels = []
    for _, y_row in y.iterrows():
        label = y_row[0]
        labels.append(label)
    result = []
    for text, label in zip(texts, labels):
        result.append((text, label))

    return result

