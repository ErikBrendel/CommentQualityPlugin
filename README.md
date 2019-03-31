# CommentQualityPlugin

This repository contains code prototypes for analyzing source code comments with machine learning techniques. It focuses on whether or not specific code parts (methods, if-statements, loops, ...) should have a comment or not, by comparing them to similar code snippets.

_A project by Anton von Weltzien and Erik Brendel_

[TOC]

## Structural overview

This project consists of three parts so far: the java program that finds ground truth data, called `java-train`, the python script collection for performing machine learning, called `python`, and the prototype of a JetBrains-Plugin, as seen in the directory `plugin`.

## Usage instructions

 - adjust the constants in `java-train / TrainingMain` (your desired clone path, number of parallel workers or which repos to check)
 - run `java-train`
 - _you should now have some data csv files at your given `REPO_CLONE_PATH`_
 - run either `analys_method_comments` or `analys_inline_comments` from `python/training` (ou might need to adjust the environment variable `CSV_ROOT`, so that the script can find the csv files). This takes some time on the first run, but further analytics should be faster (since data aggregation and completion get cached).
 - _you should see ML performance output_

## Understanding the output

Multiple classifier types are tested and evaluated against the data. Each gets introduced by `Training <classifier name>`. Where available, the importance of features in that trained classifier get printed next. The following classification report table gives an overview over the classifiers performance, a confusion matrix is printed afterwards for additional information.

## Additional outputs

A `short_tree.pdf` is generated, showing how the depth-5 classifier tree internally works. Node colors represent the tendency towards a class (needs comment / needs no comment) for all the test data samples that reached that node.

To generate software quality metrics for a whole repository, uncomment the lines containing the call to `evaluate_repo_with` in the python main files. This generates metrics (like the amount of methods in a file that should be commented according to the classifier but are not), aggregated into a single csv file. This generates the `eval_result` and `complete_result` csv files, which can be further used in e.g. visualization software.

## The Plugin

The JetBrains-Plugin is currently only a prototype and marks each comment as bad. It could, however, trigger a python script instead to use the cached trained classifier to actually check, whether code snippets would need a comment or not. A basis for this is already implemented. _(you might need to enable the inspection first under File > Settings > Editor > Inspections > Comment Quality)_
