from typing import *


class QualityComment:

    def __init__(self, method_node):
        self.method_node = method_node

    def identity(self) -> str:
        return ""

    def comment_words(self) -> List[str]:
        return []

    def code_words(self) -> List[str]:
        return []

    def full_code(self) -> str:
        return ""
