import pytest
from click.testing import CliRunner

from utils import shell


@pytest.fixture()
def project_new_runner():
    print('setup')
    runner = CliRunner()
    yield runner
    print('\nteardown')


def test_passing_only_name(project_new_runner):
    """ignore other options"""
    from commands.cmd_project import new
    from utils.testing import ClickDefaultErrorOutput as Error

    with project_new_runner.isolated_filesystem():
        result = project_new_runner.invoke(new, shell.to_args('test_projected'))

    assert Error.MISS_OPT in result.stdout


def test_passing_name_and_suited_opt_lang(project_new_runner):
    from commands.cmd_project import new

    with project_new_runner.isolated_filesystem():
        result = project_new_runner.invoke(new, shell.to_args('test_projected --lang cpp'))

    assert 'Generated the project' in result.stdout
