import os
import shlex
import subprocess
from contextlib import contextmanager
from pathlib import Path
from typing import List


@contextmanager
def change_dir_temporarily_to(dir_path: Path):
    from os import chdir
    old_dir_path = Path.cwd()
    chdir(dir_path)
    yield
    chdir(old_dir_path)


def run(command: str) -> subprocess.CompletedProcess:
    return subprocess.run(shlex.split(command))


def to_args(command: str) -> List[str]:
    return shlex.split(command)


def current_running_path() -> str:
    return os.getcwd()
