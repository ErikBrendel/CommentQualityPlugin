import javalang
from multiprocessing import Pool
from . import GitRepo

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


def parse_repo(repo_name: str):
    return len(repo_name)


with Pool(None) as p:
    result = p.map(parse_repo, REPOS)
    print(result)




# for x in range(1000):
#     print(x)
#     tree = javalang.parse.parse(code)
#     list = [x.children[0] for [p, x] in tree.filter(javalang.tree.MethodDeclaration)]
#
# print(tree)