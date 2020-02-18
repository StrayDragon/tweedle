import click


def display(msg: str,
            *,
            font_color: str = None,
            bold: bool = None,
            nl: bool = True):
    click.secho(msg, fg=font_color, bold=bold, nl=nl)


def warning():
    click.echo(
        "This implementation is unstable and may have irreversible consequences"
    )
    click.echo("If you ensure to run it, ")
    click.echo("please add '-P test' after this command.")


def displayx(msgs):
    for msg, color in msgs:
        display(msg, font_color=color, bold=False, nl=False)
