import click


@click.group('project', short_help='Generate a project structure out of the box')
def cli():
    """Generate a project structure and save a little time"""
    pass


@cli.command()
@click.argument('project_name')
@click.option('-L', '--lang', type=click.Choice(['cpp']))
@click.option('-B', '--build-tool', type=click.Choice(['cmake']))
@click.option('-T', '--third-party', type=click.Choice(['googletest']))
def new(project_name, lang, build_tool, third_party):
    """Generate a target project"""
    click.echo(
        f'Generated the "{project_name}", {lang}, {build_tool}, {third_party}')
    pass
