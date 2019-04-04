# CommentQualityPlugin

This repository contains code prototypes for analyzing source code comments with machine learning techniques. It focuses on whether or not specific code parts (methods, if-statements, loops, ...) should have a comment or not, by comparing them to similar code snippets.

_A project by Anton von Weltzien and Erik Brendel_

### Structural overview

This project consists of three parts so far: the java program that finds ground truth data, called `java-train`, the python script collection for performing machine learning, called `python`, and the prototype of a JetBrains-Plugin, as seen in the directory `plugin`.

### Usage instructions

 - adjust the constants in `java-train / TrainingMain` (your desired clone path, number of parallel workers or which repos to check)
 - run `java-train`
 - _you should now have some data csv files at your given `REPO_CLONE_PATH`_
 - run either `analyse_method_comments` or `analyse_inline_comments` from `python/training` (you might need to adjust the environment variable `CSV_ROOT`, so that the script can find the csv files). This takes some time on the first run, but further analytics should be faster (since data aggregation and completion get cached, however, the cache is not updated if the items in `CSV_ROOT` are changed. In that case delete the cache manually). 
 - _you should see ML performance output_
 - Running either `analyse_method_comments` or `analyse_inline_comments` will also generate a persisted model in the `python/training` directory. Which can then be used from `run_cached_model`. This generates metrics (like the amount of methods in a file that should be commented according to the classifier but are not), aggregated into both `eval_result` and `complete_result` csv files, which can be further used in e.g. visualization software.
 - _you should see the reasons for the decisions that were made (note that if the model is very large > 100mb this might need excessive amounts of memory and should be turned off)._

### Understanding the output

Multiple classifier types are tested and evaluated against the training set through k-fold cross validation. (The training Set contains 70% of the data). Each classifier gets introduced by `Doing <classifier name>`. An array with the evaluation score containing: classifier name with its time required to train and test, and its f1-score for train and test set will be printed. Based on this the best classifier is chosen and  Where available, the importance of features in that trained classifier get printed next. The following classification report table gives an overview over the classifier's performance, a confusion matrix is printed afterwards for additional information.

### Additional outputs

A `dtree.pdf` can be generated, showing how the decision tree classifier works internally. Node colors represent the tendency towards a class (needs comment / needs no comment) for all the test data samples that reached that node. Note that you should use the `ShortTree` for this or create you own small tree as it will be too big to view and understand otherwise. 


### The Plugin

The JetBrains-Plugin is currently only a prototype and marks each comment as bad. It could, however, trigger a python script instead to use the cached trained classifier to actually check, whether code snippets would need a comment or not. A basis for this is already implemented. _(you might need to enable the inspection first under File > Settings > Editor > Inspections > Comment Quality)_
