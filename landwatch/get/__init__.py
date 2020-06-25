import click
from .lands import download

@click.group()
def get():
    pass

get.add_command(download)

_cli = get
