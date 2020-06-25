import click

@click.command()
def get():
    click.echo("Get has been called.")

_cli = get
