#!venv/bin/python3

"""
Should print one line containing 'YES' or 'NO', depicting, whether the given code snippet
should have a comment or not, according to the classifier.
Can print additional lines with more information.
"""

import sys

[_, code_snippet, *metrics] = sys.argv

# TODO:
#  compute the additional metrics,
#  load the classifier from a pickle,
#  classify the given code snippet

print('YES')
print('[Stub] All code snippets should have comments!')
