import click
from .lands import _cli

@click.group()
def get():
    pass # pragma: no cover

get.add_command(_cli)

_cli = get
