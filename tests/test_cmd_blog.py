import pytest
from click.testing import CliRunner

from utils import shell
from mods.mod_blog import Blog


@pytest.fixture()
def blog_runner():
    # Setup
    runner = CliRunner()
    yield runner
    # Tear Down


def test_publish(blog_runner):
    from cmds.cmd_blog import publish
    with blog_runner.isolated_filesystem():
        state = blog_runner.invoke(publish, shell.to_args('-P test'))
    for cmd in Blog.publish_commands:
        assert cmd in state.output


def test_finish(blog_runner):
    from cmds.cmd_blog import finish
    with blog_runner.isolated_filesystem():
        state = blog_runner.invoke(finish, shell.to_args('-P test'))
    for cmd in Blog.finish_commands:
        assert cmd in state.output
