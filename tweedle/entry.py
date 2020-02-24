from box import Box

from tweedle import PROJECT_NAME
from tweedle.core import cli


def main():
    cli(auto_envvar_prefix=PROJECT_NAME, obj=Box(default_box=True))


if __name__ == "__main__":
    # Enable debug by using vimspector
    main()
