from munch import Munch

from . import PROJECT_NAME
from .core import cli


def main():
    cli(auto_envvar_prefix=PROJECT_NAME, obj=Munch())
