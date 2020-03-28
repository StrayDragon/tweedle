from click.testing import CliRunner


def test_simple_hook(runner: CliRunner):
    # 1. test source code init (like `eval "$(tweedle hook init)"`)
    # 2. test add hook and effect
    # 3. test remove hook and effect
    assert 1
