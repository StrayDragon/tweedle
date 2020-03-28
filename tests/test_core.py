import os
from pathlib import Path
from typing import List, Optional

import attr
import pytest
from box import Box

from tweedle import PROJECT_NAME
from tweedle.core import Tweedle
from tweedle.util import fs


@pytest.mark.usefixtures("cd_tmp_folder")
class TestTweedle:
    def test_init_with_no_config(self):
        tweedle = Tweedle.init(dev=True, dev_prefix=Path.cwd())
        assert tweedle.app_home_path is not None
        assert not tweedle.app_home_path.exists()
        config_path = tweedle.app_home_path / 'rc.toml'
        assert not config_path.exists()

    def test_init_with_spawning_default_config(self):
        tweedle = Tweedle.init(dev=True, dev_prefix=Path.cwd(), generate_default_config=True)
        assert tweedle.app_home_path is not None
        assert tweedle.app_home_path.exists()
        config_path = tweedle.app_home_path / 'rc.toml'
        assert config_path.exists()
        assert not Box.from_toml(filename=str(config_path))

    def test_init_from_exist_default_config(self):
        exist_config_path: Path = fs.get_default_app_dir(
            PROJECT_NAME,
            dev=True,
            dev_prefix=Path.cwd(),
        ) / 'rc.toml'
        expect = Tweedle.init(dev=True, dev_prefix=Path.cwd())
        exist_config_path.parent.mkdir(parents=True, exist_ok=True)
        kv = expect.as_raw_dict(filter=attr.filters.exclude(attr.fields(Tweedle).app_home_path))
        Box(**kv).to_toml(filename=str(exist_config_path), encoding='utf-8')
        actual = Tweedle.init(dev=True, dev_prefix=Path.cwd())
        # assert str(actual.app_home_path) == str(expect.app_home_path)
        assert actual == expect
