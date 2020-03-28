import logging
import shlex
from pathlib import Path
from typing import Dict, List, Set, Union

import attr
import click
import pytest
from box import Box
from click.testing import CliRunner
from box import Box
from tweedle.cmd import project
from tweedle.util import sh


@pytest.fixture
def supported_workspace():
    pass


@click.command()
def spawn():
    # 0. Get available project configs from target path (local)
    #    NOTE:
    #    - [ ] support fetch remote repo(or ...) and check configs from it
    #    - [ ] support multi schemaes interface
    #    - [ ] support customize schema loader (A way to handle file location or schema structure)
    #
    # # e.g.
    # configs_schema = \
    #           Project.load_configs_schema(schema_path) # schema is (toml,json,yaml...)
    # #         Project.load_configs_schema(root_folder_path) # for customize configs struct and path info
    # project_configs_helper: Project  = Project.retrieve_configs_from(configs_schema)

    # 1. (Optional) detect project cwd
    #    NOTE:
    #    - [ ] put high priority projects first
    #    - [ ] give suggestions when detect project root folder? (somewhere contains '.git', '.root', '.svn' ...)
    #    - [ ] support configs about default order of checkbox list
    #
    # # e.g.
    # project_configs_helper.detect_and_adjust_types_order()
    # # (view code) prompt `pws_types`

    # 2. construct dict and show configs checkboxes
    #
    # # e.g.
    # type_configs: Dict[stk, List[ProjectConfiguration]]
    # # (view code) prompt `type_configs`

    # 3. (Optional) review and confirm the items and prompts
    #
    # # e.g.
    # # (view code) prompt ``

    # 4. generate config files in project work space, done!
    #
    # # e.g.
    pass


class TweedleException(Exception):
    pass


class TweedleHome:
    @classmethod
    def load_self_config(cls):
        raise NotImplementedError

    def get_app_dir(self):
        pass

    def get_self_config_path(self):
        pass


from tweedle import PROJECT_NAME
from tweedle.util import fs

MOD_PROJECT_ROOT = fs.get_default_app_dir(PROJECT_NAME, dev=True)


# NOTE: How to sign a file to a project configuration which `tweedle` can recognize?
# Options:
# - Use metadata: inject some comments to the target file and retrieve info from it everytime?
# - Use stub file: generate a stub to describe these file structure and info
@attr.s(frozen=True)
class ProjectConfiguration:
    name: str = attr.ib()
    types: Set[str] = attr.ib(converter=set)
    description: str = attr.ib()
    relative_path: Path = attr.ib()
    config_root_path: Path = attr.ib()
    path: Path = attr.ib(init=False)

    def __attrs_post_init__(self):
        object.__setattr__(self, 'path', self.config_root_path / self.relative_path)

    @classmethod
    def from_box(cls, b: Box, config_root_path: Path = MOD_PROJECT_ROOT):
        return cls(
            config_root_path=config_root_path,
            **b,
        )


class ProjectConfigurationDB:
    def __init__(self):
        pass


class WorkspaceType(object):
    pass


class PythonWorkspaceType(WorkspaceType):
    pass


@attr.s
class Project:
    """"""
    workspace_types: Set[str] = attr.ib(factory=set, init=False)

    def _detect_current_workspace_types(self):
        if self.workspace_types: return self.workspace_types
        cwd = Path.cwd()
        for file in cwd.iterdir():
            if str(file).endswith('.py'):
                return {'python'}
        return set()

    def __attrs_post_init__(self):
        self.workspace_types = self._detect_current_workspace_types()

    @classmethod
    def retrieve_configs_from(cls, configs_schema: List[ProjectConfiguration]):
        pass


def _load_configs_schema(configs_schema_abspath: Union[str, Path]) -> Box:
    """
    Convert json|toml|yaml to Box instance

    :param configs_schema_abspath Union[str, Path]: absolute path to the file
    :rtype Box: [python-box](https://github.com/cdgriffith/Box) instance
    """
    path = Path(configs_schema_abspath)
    box_converters = {'.json': Box.from_json, '.toml': Box.from_toml, '.yaml': Box.from_yaml}
    return box_converters[path.suffix](filename=str(path))


@pytest.mark.usefixtures('cd_tmp_folder')
class TestProjectModSpawn:
    def test_loaded_correct_configs_schema(self, tmp_path: Path):
        configs_schema_raw_toml = """
        [project]
        [[project.configs]]
        name = ".vimspector"
        description = "vimspector default setting"
        types = [ "python", "c++",]
        relative_path = "python/vim/debug/.vimspector"
        """
        configs_schema_path: Path = tmp_path / '_.toml'
        configs_schema_path.write_text(configs_schema_raw_toml, encoding='utf-8')

        configs_schema: Box = _load_configs_schema(configs_schema_path)
        # __import__('pprint').pprint(configs_schema.to_dict())
        pc = ProjectConfiguration.from_box(configs_schema.project.configs[0])
        # __import__('pprint').pprint(pc)

    def test_dyn_detect_project_type(self):
        # FIXME: Only detect python workspace type
        # Inspired from starship (see: https://github.com/starship/starship https://starship.rs/config/#prompt
        #               oh-my-zsh(see: https://github.com/ohmyzsh/ohmyzsh)
        assert Project().workspace_types == set()

        flag_file: Path = Path.cwd() / 'test.py'
        flag_file.touch(exist_ok=True)
        assert Project().workspace_types == {'python'}


# class TestProjectCLI:
#     def test_basic(self, runner: CliRunner):
#         result = runner.invoke(project.cli, ['-s'])
#         assert 'Error: no such option' not in result.output
#         assert result.exit_code == 0
#         with pytest.raises(TypeError):
#             pass
#         pass
#     pass
