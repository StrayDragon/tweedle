import pytest
from pytest_mock import mocker
from utils import shell


def test_shell_run(mocker):
    mocker.patch('utils.shell.run')
    shell.run('ls -l')


def test_shell_to_args():
    expected = ['ls', '-l']
    result = shell.to_args('ls -l')
    assert result == expected


def test_terminal_printx():
    from utils.terminal import Colors, printx
    some_log = [('This is red ', Colors.Magenta),
                ('This is Blue', Colors.Blue)]
    printx(some_log)
