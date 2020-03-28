import pytest
from click.testing import CliRunner

from tweedle.core import cli
from tweedle.cmd import project
from tweedle.cmd import blog


@pytest.mark.parametrize('cli', [
    cli,
    project.cli,
    blog.cli,
])
def test_subcmd(runner: CliRunner, cli):
    with runner.isolated_filesystem():
        result = runner.invoke(cli, '--help')
        assert result.exit_code == 0
        assert 'Usage:' in result.stdout
