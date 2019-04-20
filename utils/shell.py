import os
import shlex
import subprocess
from functools import wraps, partial
from typing import List


def run(command: str) -> subprocess.CompletedProcess:
    return subprocess.run(shlex.split(command))


def to_args(command: str) -> List[str]:
    return shlex.split(command)


def current_running_path() -> str:
    return os.getcwd()


def check_external_program(command: str = None):
    """
    A decorator use to check required commands.
    :param command: program name
    """

    #
    # Execute code when define a wrapped function.
    #
    def decorate(f):
        #
        # Execute code when invoke the wrapped function,
        #
        result = subprocess.getstatusoutput(command)

        @wraps(f)
        def wrapper(*args, **kwargs):
            if 'not found' in result[1]:
                raise Exception(f"Error: '{command}' is not exist!")
            return f(*args, **kwargs)

        return wrapper

    if not isinstance(command, str):
        print('@check_external_program')
        # Plan 1
        # raise Exception('Can not use non-parameters decorator')
        # Plan 2
        f = command
        return f

    return decorate
