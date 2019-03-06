from pandas import DataFrame
from sklearn import tree
import graphviz



def classify_by_dTree(x_train: DataFrame, y_train: DataFrame, x_test: DataFrame,
                      should_print=True) -> DataFrame:
    # cols = [col for col in frame.columns.tolist() if col not in ['commented', 'comment']]
    # X = frame[cols]
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(x_train, y_train)
    predicted = clf.predict(x_test)
    if should_print:
        dot_data = tree.export_graphviz(clf, out_file=None)
        graph = graphviz.Source(dot_data)
        graph.render("iris")
    return predicted
