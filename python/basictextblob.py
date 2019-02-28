from textblob import TextBlob
from typing import *
from textblob import Word
from textblob.classifiers import DecisionTreeClassifier, NaiveBayesClassifier

def run_textBlob(train, test):

    def to_word_list(word_list: str):
        words = word_list.split(',')
        words = [Word(word).lemmatize() for word in words]
        return words


    def basic_metrics(words: List[str]) -> List[int]:
        l = len(words)
        s = set(words)
        ul = len(s)
        return [l, ul, l / ul]


    def feature_extractor(word_lists: List[str]):
        [comment, code] = word_lists
        comment_words = to_word_list(comment)
        code_words = to_word_list(code)
        comment_set = set(comment_words)
        code_set = set(code_words)
        set_inters = code_set.intersection(comment_set)

        comment_metrics = basic_metrics(comment_words)
        code_metrics = basic_metrics(code_words)

        return {
            "lengths": comment_metrics[0] / code_metrics[0],
            "uniqueLengths": comment_metrics[1] / code_metrics[1],
            "uniqueness": comment_metrics[2] / code_metrics[2],
            "overlap1": len(set_inters) / len(comment_set),
            "overlap2": len(set_inters) / len(code_set),
        }


    dtree_model = DecisionTreeClassifier(train, feature_extractor)
    print(dtree_model.pprint())
    print(dtree_model.accuracy(test))

    bayes_model = NaiveBayesClassifier(train, feature_extractor)
    print(bayes_model.accuracy(test))