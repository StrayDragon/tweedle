#!/usr/bin/env python3
from pathlib import Path

import click
from box import Box

ECHO_PREFIX = f'[gen_stub] '


@click.group()
def cli():
    pass


def read_and_create_stub(*args, dest=Path.cwd()):
    a, n, h, p = args

    b = Box(default_box=True)

    b.name = a
    b.executable_name = n
    # b.management.install['from'] = 'a'
    b.management.config.habitual_path = h
    b.management.config.lookup_paths = p

    dest = dest / f"{b.name}.toml"
    click.secho(ECHO_PREFIX + f'writing to {dest}...')
    b.to_toml(filename=dest)


@cli.command()
def tutor():
    click.secho(ECHO_PREFIX + 'A tutor to create stub:')
    appname = click.prompt(ECHO_PREFIX + 'input the app name which you want to manage')
    appexename = click.prompt(ECHO_PREFIX + 'input this app executable name')
    if click.confirm(ECHO_PREFIX + 'has config section ?', abort=True, default=True):
        habitual_path = click.prompt(ECHO_PREFIX + 'input the habitual_path')

        click.secho(ECHO_PREFIX + 'Will open a tempfile to record the app configs lookup paths')
        click.pause()
        COMMENT = '# write the paths line by line with no char end of each line'
        input_lookup_paths: str = click.edit(COMMENT)
        if input_lookup_paths is not None:
            lookup_paths = input_lookup_paths.split(COMMENT, 1)[1:][0].split('\n')
            lookup_paths = [p for p in lookup_paths if p]
            read_and_create_stub(appname, appexename, habitual_path, lookup_paths)


@cli.command()
def upgrade():
    # old_b = Box.from_toml(filename='', default_box=True)
    pass


if __name__ == "__main__":
    cli()
