import os
import sys

import click

CMD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                          'commands'))


class DragonCLI(click.MultiCommand):

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(CMD_FOLDER):
            if filename.endswith('.py') and \
                    filename.startswith('cmd_'):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            mod = __import__('commands.cmd_' + name,
                             None, None, ['cli'])
        except ImportError as e:
            raise Exception('Subcmd ImportError') from e
        return mod.cli


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
