import pytest
from click.testing import CliRunner


@pytest.mark.skip(reason="At present, I have not found a suitable way to test real commands...")
def test_publish():
    from commands.cmd_blog import publish
    runner = CliRunner()
    after_call = runner.invoke(publish)
    result = after_call.exit_code
    expected = 0
    assert expected == result


@pytest.mark.skip(reason="At present, I have not found a suitable way to test real commands...")
def test_finish():
    from commands.cmd_blog import finish
    runner = CliRunner()
    after_call = runner.invoke(finish)
    result = after_call.exit_code
    expected = 0
    assert expected == result
