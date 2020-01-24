import os
import shlex
import subprocess
from functools import partial, wraps
from pathlib import Path
from typing import List, Callable

import click


def find_osenv_by_key(name: str,
                      default: str = '') -> Callable[[str, str], str]:
    """used to replace <lambda> of click.option() `default=<lambda>`"""
    def _get_os_env(k, default_v):
        return os.environ.get(k, default_v)

    return partial(_get_os_env, k=name, default_v=default)


def get_project_root() -> Path:
    """Returns project root folder."""
    return Path(__file__).parent.parent


def get_project_src() -> Path:
    """Returns project source folder."""
    return Path(__file__).parent


def get_project_tests() -> Path:
    """Returns project tests folder."""
    return Path(__file__).parent / 'tests'


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


def log(msg: str,
        *,
        font_color: str = None,
        bold: bool = None,
        nl: bool = True):
    click.echo(click.style(msg, fg=font_color, bold=bold), nl=nl)


def log_of_warning():
    click.echo(
        "This implementation is unstable and may have irreversible consequences"
    )
    click.echo("If you ensure to run it, ")
    click.echo("please add '-P test' after this command.")


class Colors:
    Black = 'black'
    Gray = 'black'
    Green = 'green'
    Yellow = 'yellow'
    Blue = 'blue'
    Magenta = 'magenta'
    Cyan = 'cyan'
    White = 'white'
    LightGray = 'white'
    RESET = 'reset'


def printx(msgs):
    for msg, color in msgs:
        log(msg, font_color=color, bold=False, nl=False)


class ClickDefaultErrorOutput(object):
    MISS_OPT = 'Missing option'
    NO_OPT = 'no such option:'
    RQR_OPT = 'option requires an argument'
    CHOOSE_OPT = 'invalid choice'
