import click

@click.group(
    help = "Get bills and legislator data relevant to parcels"
    " of American public fee lands under federal management."
)
@click.pass_context
def bills(ctx):
    pass

@bills.command(
    help="Query ProPublica API for bills relevant to parcels of land"
    " and output them as a sqlite db."
)
@click.argument("lands")
@click.argument("dest")
@click.option("--api-key", help="ProPublica Congress API key.")
@click.pass_context
def download(ctx, lands, dest):
    pass
