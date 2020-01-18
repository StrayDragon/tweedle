import click

from ..mods.mod_blog import Blog
from ..utils.terminal import log_of_warning


@click.group('blog', short_help='Control the Hexo-based blog system')
def cli():
    """A bundle of daily commands of using the Hexo to manage blog"""
    pass


@cli.command()
@click.option('-P', '--protected', default=True)
def publish(protected):
    """Publish blog easily"""
    if protected is True:
        log_of_warning()
        return
    Blog.publish()


@cli.command()
@click.option('-P', '--protected', default=True)
def finish(protected):
    """Update blog repo state to Github"""
    if protected is True:
        log_of_warning()
        return
    Blog.finish()
