from importlib import import_module
from pathlib import Path

import click

SUBCMDS_FOLDER = Path('.') / 'src' / 'cmds'


class DragonCLI(click.MultiCommand):
    def list_commands(self, ctx):
        return [str(x.name)[:-3] for x in SUBCMDS_FOLDER.glob('*.py')]

    def get_command(self, ctx, name):
        mod = import_module(name=f'src.cmds.{name}')
        return getattr(mod, 'cli')


@click.command(cls=DragonCLI)
@click.version_option()
@click.help_option()
# @click.pass_context
def cli():
    """Welcome to use Dragon-CLI, enjoy it and be efficient :P"""
    pass


def main():
    cli()


if __name__ == '__main__':
    main()
