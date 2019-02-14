import shlex
import subprocess
from subprocess import CompletedProcess

import click


def hexo_cmd_not_pass(cp: CompletedProcess):
    """
    FIXME: Will refactor
    :param cp:
    :return:
    """
    msg = cp.stdout or cp.stderr or b''
    return b'Usage: hexo <command>' in msg


def log(msg: str, *, fg: str = None, bold=None, nl=True):
    click.echo(click.style(msg, fg=fg, bold=bold), nl=nl)


class Blog(object):
    PASS = '[Ok]'
    NOT_PASS = '[Fail]'
    main_cmd = 'hexo'

    publish_commands = ('hexo clean', 'hexo g -d', 'hexo clean', 'rm .deploy_git -rf')
    finish_commands = ('git add -A', 'git commit -m "update blog"', 'git push')

    @staticmethod
    def publish():
        result = True
        for command in Blog.publish_commands:
            log(f"Current Running Command: '{command}' ... ", fg='green', bold=True)
            cp: CompletedProcess = subprocess.run(shlex.split(command))
            if hexo_cmd_not_pass(cp):
                result = False
        return result

    @staticmethod
    def finish():
        result = True
        for command in Blog.finish_commands:
            log(f"Current Running Command: '{command}' ... ", fg='green', bold=True)
            cp: CompletedProcess = subprocess.run(shlex.split(command))
        return result


@click.group('blog', short_help='Control the Hexo-based blog system')
def cli():
    """A bundle of daily commands of using the Hexo to manage blog"""
    pass


@cli.command()
@click.option('-P', '--protected', default=True)
def publish(protected):
    """Publish blog easily"""
    if protected is True:
        click.echo("This implementation is unstable and may have irreversible consequences")
        click.echo("If you ensure to run it, ")
        click.echo("please add '-P test' after this command.")
        return
    Blog.publish()


@cli.command()
@click.option('-P', '--protected', default=True)
def finish(protected):
    """Update blog repo state to Github"""
    if protected is True:
        click.echo("This implementation is unstable and may have irreversible consequences")
        click.echo("If you ensure to run it, ")
        click.echo("please add '-P test' after this command.")
        return
    Blog.finish()
