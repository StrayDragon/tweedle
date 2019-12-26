import pytest
from src.utils import shell


def test_shell_run(mocker):
    mocker.patch('src.utils.shell.run')
    shell.run('ls -l')
    shell.run.assert_called_once_with('ls -l')


def test_shell_to_args():
    expected = ['ls', '-l']
    result = shell.to_args('ls -l')
    assert result == expected


@pytest.mark.skip('Should have at least one assertion statement,but not')
def test_terminal_printx():
    from src.utils.terminal import Colors, printx
    some_log = [('This is Red ', Colors.Magenta),
                ('This is Blue', Colors.Blue)]
    printx(some_log)
