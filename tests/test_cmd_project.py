import pytest
from click.testing import CliRunner

from src.utils import shell


@pytest.fixture()
def project_new_runner():
    # Setup
    runner = CliRunner()
    yield runner
    # Tear Down


@pytest.mark.skip('Will rewrite,refer: line 13 in cmd_project')
def test_passing_only_name(project_new_runner):
    """
    $ dragon project new test_projected
    """
    from src.cmds.cmd_project import new
    from src.utils.testing import ClickDefaultErrorOutput as Error

    with project_new_runner.isolated_filesystem():
        result = project_new_runner.invoke(new,
                                           shell.to_args('test_projected'))

    assert Error.MISS_OPT in result.stdout


@pytest.mark.skip('Will rewrite,refer: line 13 in cmd_project')
def test_passing_name_and_suited_opt_lang(project_new_runner):
    """
    $ dragon project new test_projected --lang cpp
    """
    import os
    from src.cmds.cmd_project import new

    with project_new_runner.isolated_filesystem():
        result = project_new_runner.invoke(
            new, shell.to_args('test_projected --lang cpp'))
        project_root_dir_exist = os.path.exists(
            os.path.join(os.getcwd(), 'test_projected'))

    assert project_root_dir_exist
    assert 'Generated the project' in result.stdout
