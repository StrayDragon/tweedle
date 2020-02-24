__all__ = ["cli"]

from importlib import import_module

import click

from tweedle import PROJECT_SRC, __version__
from tweedle.util import clickx

SUBCMDS_FOLDER = PROJECT_SRC / 'cmd'


class TweedleSubCommandsCLI(click.MultiCommand):
    def list_commands(self, ctx):
        # return [
        #     str(x.name)[:-3] for x in SUBCMDS_FOLDER.glob('*.py')
        #     if not x.name.startswith('__init__')
        # ]
        subcmds = ['manage']
        return subcmds

    def get_command(self, ctx, name):
        mod = import_module(name=f'.cmd.{name}', package='tweedle')
        return getattr(mod, 'cli')


@click.command(name='tweedle', cls=TweedleSubCommandsCLI)
@click.version_option(help='show version details', version=__version__)
@clickx.option_of_common_help
def cli():
    """
    Welcome to use tweedle, enjoy it and be efficient :P\n
    Please use "tweedle COMMAND --help" to get more detail of usages
    """
    pass
