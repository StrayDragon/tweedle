import os
import shlex
import subprocess
from functools import wraps
from typing import List


def run(command: str) -> subprocess.CompletedProcess:
    return subprocess.run(shlex.split(command))


def to_args(command: str) -> List[str]:
    return shlex.split(command)


def current_running_path() -> str:
    return os.getcwd()


def check_command(command: str):
    def decorate(f):
        result = subprocess.getstatusoutput(command)

        @wraps(f)
        def wrapper(*args, **kwargs):
            if 'not found' in result[1]:
                return f(*args, **kwargs)
            raise Exception(f"Error: '{command}' is not exist!")

        return wrapper

    return decorate
