import click


def log(msg: str, *, font_color: str = None, bold: bool = None, nl: bool = True):
    click.echo(click.style(msg, fg=font_color, bold=bold), nl=nl)


def log_of_warning():
    click.echo(
        "This implementation is unstable and may have irreversible consequences")
    click.echo("If you ensure to run it, ")
    click.echo("please add '-P test' after this command.")


class Colors:
    Black = 'black'
    Gray = 'black'
    Green = 'green'
    Yellow = 'yellow'
    Blue = 'blue'
    Magenta = 'magenta'
    Cyan = 'cyan'
    White = 'white'
    LightGray = 'white'
    RESET = 'reset'


def printx(msgs):
    for msg, color in msgs:
        log(msg, font_color=color, bold=False, nl=False)
