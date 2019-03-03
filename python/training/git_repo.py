import os
from typing import *

from .ExternalProgram import ExternalProgram

REPO_CLONE_PATH = "repos/"
REPO_URL_START = "https://github.com/"
REPO_URL_END = ".git"


def pretty_filename(raw_name):
    if raw_name.startswith('./'):
        return raw_name[2:]
    return raw_name


def is_filename(raw_name):
    return len(raw_name) > 3


class GitRepo:
    def __init__(self, name: str):
        self.name = name
        self.localProgram = ExternalProgram(self.root_directory())

    def program(self) -> ExternalProgram:
        return self.localProgram

    def root_directory(self):
        return os.path.abspath(REPO_CLONE_PATH + self.escaped_name())

    def escaped_name(self) -> str:
        return self.name.replace('/', '-')

    def update(self):
        if not self.is_cloned():
            self.clone()
        else:
            self.pull()

    def find_files(self) -> List[str]:
        found_files = self.localProgram.run_args(["find", ".", "-name", "*.java"])
        found_files = [file for file in found_files if 'test' not in file]
        return [pretty_filename(file) for file in found_files if is_filename(file)]

    def is_cloned(self):
        return os.path.exists(self.root_directory())

    def clone(self):
        os.mkdir(self.root_directory())
        git_url = REPO_URL_START + self.name + REPO_URL_END
        print(self.localProgram.run_args_joined(["git", "clone", git_url, self.root_directory()]))

    def pull(self):
        print(self.name + ": " + self.localProgram.run_joined("git pull"))
