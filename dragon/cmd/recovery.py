import click


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.secho("Start to recovery this operator system", fg="green")
    else:
        click.secho("Subcommands invoke successfully", fg="yellow")


@cli.command()
def info():
    click.secho("info searing...", fg='green')
