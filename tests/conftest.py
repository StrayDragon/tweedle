from typing import Generator

import pytest
from click.testing import CliRunner


@pytest.fixture
def cli_runner():
    # setup
    yield CliRunner()
    # teardown
