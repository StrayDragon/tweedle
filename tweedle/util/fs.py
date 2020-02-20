from pathlib import Path


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


if __name__ == "__main__":
    print("hello vimspector")
    a = get_project_src()
    print(a)
