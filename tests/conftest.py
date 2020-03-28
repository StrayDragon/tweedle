import os
import shutil
import tempfile
from pathlib import Path
from typing import Generator

import pytest
from click.testing import CliRunner


@pytest.fixture(scope="function")
def cli_runner():
    # setup
    yield CliRunner()
    # teardown


@pytest.fixture(scope="function")
def runner():
    # setup
    yield CliRunner()
    # teardown


@pytest.fixture
def cd_tmp_folder():
    old = Path.cwd()
    new = tempfile.mkdtemp()
    os.chdir(new)
    yield
    os.chdir(old)
    shutil.rmtree(new)


# https://unix.stackexchange.com/questions/326766/what-are-the-standard-error-codes-in-linux
