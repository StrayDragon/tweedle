from pathlib import Path

import click


def strip_ext(filename: str) -> str:
    """Remove file extension name, like 'a.c' -> 'a'"""
    return filename[:filename.rfind('.')]


def get_project_root() -> Path:
    """Returns project root folder."""
    return Path(__file__).parent.parent.parent


def get_project_src() -> Path:
    """Returns project source folder."""
    return Path(__file__).parent.parent


def get_project_tests() -> Path:
    """Returns project tests folder."""
    return Path(__file__).parent.parent.parent / 'tests'


def get_default_app_dir(name: str, *, dev: bool = False, dev_prefix=None) -> Path:
    from tempfile import gettempdir
    app_dir_path = Path(click.get_app_dir(name))
    if dev:
        if dev_prefix:
            return Path(dev_prefix).joinpath(*app_dir_path.parts[1:])
        return Path(gettempdir()).joinpath(*app_dir_path.parts[1:])
    return app_dir_path


if __name__ == "__main__":
    print("hello vimspector")
    a = get_project_src()
    print(a)
