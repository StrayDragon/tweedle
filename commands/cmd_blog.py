import click


@click.group('blog', short_help='Control the Hexo-based blog')
def cli():
    """A bundle of daily commands of using the Hexo to manage blog"""
    pass


@cli.command()
def publish():
    """Publish blog easily"""
    pass


@cli.command()
def update():
    """Update blog repo state to Github"""
    pass
