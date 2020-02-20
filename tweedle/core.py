__all__ = ["cli"]

from importlib import import_module

import click

from tweedle import PROJECT_SRC, __version__

SUBCMDS_FOLDER = PROJECT_SRC / 'cmd'


class TweedleSubCommandsCLI(click.MultiCommand):
    def list_commands(self, ctx):
        return [
            str(x.name)[:-3] for x in SUBCMDS_FOLDER.glob('*.py')
            if not x.name.startswith('__init__')
        ]

    def get_command(self, ctx, name):
        mod = import_module(name=f'.cmd.{name}', package='tweedle')
        return getattr(mod, 'cli')


@click.command(name='Dragon', cls=TweedleSubCommandsCLI)
@click.version_option(version=__version__)
@click.help_option()
def cli():
    """Welcome to use Dragon, enjoy it and be efficient :P"""
    pass
