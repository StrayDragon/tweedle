import subprocess

import pytest
from click.testing import CliRunner

from tweedle.cmd.blog import Blog
from tweedle.util import sh


def check_command_invokable(*commands) -> bool:
    for command in commands:
        result = subprocess.getstatusoutput(command)
        if 'not found' in result[1]:
            return True
    return False


import click


@click.command()
def edit():
    pass


class TestManageBlog(object):
    def test_create_new_blog(self, cli_runner: CliRunner):
        cli_runner.invoke(edit)
        pass


@pytest.mark.skipif(condition=check_command_invokable('hexo'),
                    reason=f"Command: 'hexo' may not satisfied in local environment. skip test!")
def test_publish(cli_runner: CliRunner):
    from tweedle.cmd.blog import publish
    with cli_runner.isolated_filesystem():
        state = cli_runner.invoke(publish, sh.to_args('-P test'))
    for cmd in Blog.publish_commands:
        assert cmd in state.output


@pytest.mark.skipif(
    condition=check_command_invokable('hexo', 'git'),
    reason=f"Command: 'hexo' or 'git' may not satisfied in local environment. skip test!")
def test_finish(cli_runner: CliRunner):
    from tweedle.cmd.blog import finish
    with cli_runner.isolated_filesystem():
        state = cli_runner.invoke(finish, sh.to_args('-P test'))
    for cmd in Blog.finish_commands:
        assert cmd in state.output
