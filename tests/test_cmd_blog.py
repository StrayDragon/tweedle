import subprocess

import pytest
from click.testing import CliRunner

from dragon.utils import to_args
from dragon.cmd.blog import Blog


def check_command_invokable(*commands) -> bool:
    for command in commands:
        result = subprocess.getstatusoutput(command)
        if 'not found' in result[1]:
            return True
    return False


@pytest.fixture(scope="module")
def blog_runner():
    # Setup
    runner = CliRunner()
    yield runner
    # Tear Down


@pytest.mark.skipif(
    condition=check_command_invokable('hexo'),
    reason=f"Command: 'hexo' may not satisfied in local environment. skip test!"
)
def test_publish(blog_runner):
    from dragon.cmd.blog import publish
    with blog_runner.isolated_filesystem():
        state = blog_runner.invoke(publish, to_args('-P test'))
    for cmd in Blog.publish_commands:
        assert cmd in state.output


@pytest.mark.skipif(
    condition=check_command_invokable('hexo', 'git'),
    reason=
    f"Command: 'hexo' or 'git' may not satisfied in local environment. skip test!"
)
def test_finish(blog_runner):
    from dragon.cmd.blog import finish
    with blog_runner.isolated_filesystem():
        state = blog_runner.invoke(finish, to_args('-P test'))
    for cmd in Blog.finish_commands:
        assert cmd in state.output
