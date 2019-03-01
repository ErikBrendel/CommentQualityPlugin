import subprocess
from typing import *


class ExternalProgram:
    def __init__(self, working_dir: str = None):
        self.working_dir = working_dir

    def run_args_joined(self, command: List[str]) -> str:
        out = subprocess.check_output(command, cwd=self.working_dir)
        return out.decode("utf-8").strip()

    def run_joined(self, command: str) -> str:
        return self.run_args_joined(command.split(" "))

    def run(self, command: str) -> List[str]:
        joined = self.run_joined(command)
        if len(joined) == 0:
            return []
        return joined.split('\n')

    def run_args(self, command: List[str]) -> List[str]:
        joined = self.run_args_joined(command)
        if len(joined) == 0:
            return []
        return joined.split('\n')
