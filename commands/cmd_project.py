import click

from utils.terminal import log
from utils.shell import current_running_path


@click.group('project', short_help='Generate a project structure out of the box')
def cli():
    """Generate a project structure and save a little time"""
    pass


@cli.command()
@click.argument('project_name')
@click.option('-L', '--lang', type=click.Choice(['cpp']), required=True)
@click.option('-B', '--build-tool', type=click.Choice(['cmake']))
@click.option('-T', '--third-party', type=click.Choice(['googletest']))
def new(project_name, lang, build_tool, third_party):
    """Generate a target project"""

    # Display these after success
    log('Generated the project in ', font_color='green', bold=True, nl=False)
    log(current_running_path())
    log(f'  Project Name : {project_name}')
    log(f'  Language     : {lang}')
    if build_tool:
        log(f'  Build Tool   : {build_tool}')
    if third_party:
        log(f'  External-Libs: {third_party}')
