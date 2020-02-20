import click

from tweedle.util import cliview, sh


class Blog(object):
    PASS = '[Ok]'
    NOT_PASS = '[Fail]'
    BASED_CMD = 'hexo'

    publish_commands = ('hexo clean', 'hexo g -d', 'hexo clean', 'rm .deploy_git -rf')

    @staticmethod
    def publish():
        for command in Blog.publish_commands:
            cliview.display(f"Current Running Command: '{command}' ... ",
                            font_color='green',
                            bold=True)
            sh.run(command)

    finish_commands = ('git add -A', 'git commit -m "update blog"', 'git push')

    @staticmethod
    def finish():
        for command in Blog.finish_commands:
            cliview.display(f"Current Running Command: '{command}' ... ",
                            font_color='green',
                            bold=True)
            sh.run(command)


@click.group('blog', short_help='Control the Hexo-based blog system')
def cli():
    """A bundle of daily commands of using the Hexo to manage blog"""
    pass


@cli.command()
@click.option('-P', '--protected', default=True)
def publish(protected):
    """Publish blog easily"""
    if protected is True:
        cliview.warning()
        return
    Blog.publish()


@cli.command()
@click.option('-P', '--protected', default=True)
def finish(protected):
    """Update blog repo state to Github"""
    if protected is True:
        cliview.warning()
        return
    Blog.finish()
