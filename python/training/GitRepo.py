from .ExternalProgram import ExternalProgram

REPO_CLONE_PATH = "/home/erik/Documents/repos/qualityCommentRepos/"
REPO_URL_START = "https://github.com/"
REPO_URL_END = ".git"


class GitRepo:
    def __init__(self, name):
        self.name = name
        self.localProgram = ExternalProgram(self.root_directory())

    def root_directory(self):
        return REPO_CLONE_PATH + self.name.replace('/', '-')

    def update(self):
        if not self.isCloned():
            self.clone()
        else:
            self.pull()
