import os
import subprocess
from functools import partial, wraps
from typing import Callable


def find_osenv_by_key(name: str, default: str = '') -> Callable[[str, str], str]:
    """used to replace <lambda> of click.option() `default=<lambda>`"""
    def _get_os_env(k, default_v):
        return os.environ.get(k, default_v)

    return partial(_get_os_env, k=name, default_v=default)


def check_external_program(command: str = None):
    """
    A decorator use to check required commands.
    :param command: program name
    """
    def decorate(f):
        result = subprocess.getstatusoutput(command)

        @wraps(f)
        def wrapper(*args, **kwargs):
            if 'not found' in result[1]:
                raise Exception(f"Error: '{command}' is not exist!")
            return f(*args, **kwargs)

        return wrapper

    if not isinstance(command, str):
        print('@check_external_program')
        f = command
        return f

    return decorate
