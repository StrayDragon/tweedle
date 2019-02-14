import pytest
from click.testing import CliRunner


@pytest.fixture
def blog_fixture():
    pass


def test_blog_publish():
    from commands.cmd_blog import publish, Blog
    runner = CliRunner()
    after_call = runner.invoke(publish)
    result = (after_call.exit_code, Blog.PASS in after_call.output)
    expected = (0, False)
    assert expected == result

# def test_blog_update():
#     assert Blog.update() is False
