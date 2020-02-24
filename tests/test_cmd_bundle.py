import pytest
from tweedle.util import sh
from click.testing import CliRunner

toml_txt = """
# Blog.publish()
bundle_name = "Blog System: Quick publish"

execute_cmd = [
  "hexo clean",
  "hexo g -d",
  "hexo clean",
  "rm .deploy_git -rf"
]
"""


def test_study_basic():
    import toml
    parsed_toml = toml.loads(toml_txt)
    for kv in parsed_toml.items():
        print(kv)

    assert len(parsed_toml) == 2


def test_common_cmd(mocker):
    runner = CliRunner()
    with runner.isolated_filesystem():
        mocked = mocker.patch('tweedle.util.sh.run')
        sh.run('ls -l')
        assert mocked.called
        sh.run.assert_called_once_with('ls -l')


@pytest.mark.skip()
def test_shell_converter():
    from box import Box
    from typing import List
    bundle_info = Box.from_toml('../tweedle/res/bundles/dkr.toml')

    def export(target: List[Box], to=None, strategy=None):
        assert strategy, "Required a strategy for choosing a way to export!"
        return strategy(target)

    def pack_to_shell(b):
        res = ''
        for _ in b:
            res += _
        return res

    shells = [f"# {cmd.name}\n{cmd.exec.strip()}\n" for cmd in bundle_info.Scripts]

    expected = """# Startup Tomcat8.5 Web Server and map to port:8888\ndocker run -it -p 8888:8080 tomcat:8.5\n# Startup MySQL Server and map to port:6033\ndocker run --name mysql5.7 -p 6033:3306 -e MYSQL_ROOT_PASSWORD=123456 -d mysql:5.7\n"""
    result = export(shells, strategy=pack_to_shell)
    assert result == expected
