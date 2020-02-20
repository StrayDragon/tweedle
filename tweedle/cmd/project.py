import click

from tweedle.util import cliview, sh


@click.group('project', short_help='Generate a project structure out of the box')
def cli():
    """Generate a project structure and save a little time"""
    pass


# TODO:[Refactor] Will delegate to the cookiecutter(https://github.com/audreyr/cookiecutter) project
@cli.command()
@click.argument('project_name')
@click.option('-L', '--lang', type=click.Choice(['cpp']), required=True)
@click.option('-B', '--build-tool', type=click.Choice(['cmake']))
@click.option('-T', '--third-party', type=click.Choice(['googletest']))
def new(project_name, lang, build_tool, third_party):
    """Generate a target project"""
    import os
    cur_path = os.getcwd()
    os.mkdir(os.path.join(cur_path, project_name))

    # Display these after success
    cliview.display('Generated the project in ',
                    font_color=cliview.Colors.Green,
                    bold=True,
                    nl=False)
    cliview.display(sh.current_running_path())
    cliview.display(f'  Project Name : {project_name}')
    cliview.display(f'  Language     : {lang}')
    if build_tool:
        cliview.display(f'  Build Tool   : {build_tool}')
    if third_party:
        cliview.display(f'  External-Libs: {third_party}')
