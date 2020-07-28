import click
from .lands import _cli as lands_cli
from .bills import _cli as bills_cli

@click.group()
def get():
    pass # pragma: no cover

get.add_command(lands_cli)
get.add_command(bills_cli)

_cli = get
