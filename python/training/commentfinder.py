import javalang
from multiprocessing import Pool
from training.git_repo import GitRepo
from training.quality_comment import QualityComment
from typing import *
import pandas as pd
import sys

REPOS = [  # their clone url is REPO_URL_START + this string + REPO_URL_END
    "apache/flink",
    "apache/camel",
    "elastic/elasticsearch",
    "spring-projects/spring-boot",
    "spring-projects/spring-framework",
    "square/okhttp",  # that's a small one
]


# find more at:
# https://github.com/search?l=Java&o=desc&q=pushed%3A%3E2019-02-25&s=stars&type=Repositories


def find_comment_versions(filename, program, versions_and_dates) -> Dict[str, List[Tuple[int, QualityComment]]]:
    found_comments = {}  # Dictionary[comment_id, List[[timestamp, comment]]]
    for versionAndDate in versions_and_dates:
        version_and_date_data = versionAndDate.split(" ")
        version = version_and_date_data[0]
        timestamp = int(version_and_date_data[1])

        file_content = program.run_args_joined(["git", "show", version + ":" + filename])
        file_ast = javalang.parse.parse(file_content)

        file_methods = [element for [_path, element] in file_ast.filter(javalang.tree.MethodDeclaration)]

        for method in file_methods:
            qc = QualityComment(method)
            qc_id = qc.identity()
            if qc_id not in found_comments:
                found_comments[qc_id] = []
            found_comments[qc_id].append((timestamp, qc))
    return found_comments


def extract_comments(repo: GitRepo, filename: str) -> List:
    program = repo.program()
    versions_and_dates = program.run_args(["git", "log", "--format=%H %ct", "--reverse", "--first-parent", filename])
    if len(versions_and_dates) <= 2:
        return []

    found_comments = find_comment_versions(filename, program, versions_and_dates)
    if len(found_comments) == 0:
        return []

    for qc_id in found_comments.keys():
        if len(found_comments[qc_id]) < 2:
            del found_comments[qc_id]
    if len(found_comments) == 0:
        return []

    comments = []
    for qc_id, appearances in found_comments.items():
        for appearance in appearances:
            (timestamp, qc) = appearance
            comments.append([qc_id, timestamp, qc.comment_words(), qc.code_words(), qc.full_code()])

    return comments


def parse_repo(repo_name: str):
    repo = GitRepo(repo_name)
    repo.update()
    files = repo.find_files()
    df = pd.DataFrame(columns=["id", "timestamp", "comment_words", "code_words", "code_full"])
    for file in files:
        print(repo_name + "///" + file)
        try:
            for comment in extract_comments(repo, file):
                df.append(comment)
        except:
            print("cannot parse " + file, file=sys.stderr)
    df.to_pickle("pickles/" + repo.escaped_name())
    return df.count


def train():
    with Pool(None) as p:
        result = p.map(parse_repo, REPOS)
        print(sum([x for x in result]))


if __name__ == '__main__':
    train()

# for x in range(1000):
#     print(x)
#     tree = javalang.parse.parse(code)
#     list = [x.children[0] for [p, x] in tree.filter(javalang.tree.MethodDeclaration)]
#
# print(tree)
