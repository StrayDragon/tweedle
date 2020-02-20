from munch import Munch

from tweedle import PROJECT_NAME
from tweedle.core import cli


def main():
    cli(auto_envvar_prefix=PROJECT_NAME, obj=Munch())


if __name__ == "__main__":
    # Enable debug by using vimspector
    main()
