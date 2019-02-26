from click.testing import CliRunner

from utils import shell

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
        mocked = mocker.patch('utils.shell.run')
        shell.run('ls -l')
        assert mocked.called
        shell.run.assert_called_once_with('ls -l')
