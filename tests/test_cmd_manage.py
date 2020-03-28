import pytest
from click.testing import CliRunner
from typing import *
from box import Box
from pathlib import Path
from tweedle.cmd import manage


def _make_archived_user_data(*data_paths: Union[Path, str]) -> Tuple[Path, List[Path]]:
    # make recovery stub
    b = Box(default_box=True)
    b.backup.archive_file.auto_recovery = True
    b.recovery.archive_file.irrelevant_recovery_paths = []
    b.to_toml(manage.BACKUP_RECOVERY_METAINFO_FILE_NAME)

    arcpath = Path()
    expected_paths = [Path()]
    return (arcpath, expected_paths)


def test_manage_recovery_archive_data(runner: CliRunner):
    pass
