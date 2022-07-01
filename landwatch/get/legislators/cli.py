import click

from loguru import logger

from prefect import flow
from .legislators import process_legislators

@click.group(
    help = "Get metadata for legislators relevant to bills"
    " located in a database from the ProPublica API."
)
@click.pass_context
def legislators(ctx):
    pass

@legislators.command("download")
@click.argument("bills_db")
@click.option(
    "--newdb",
    is_flag=True,
    help= (
        "Create a standalone sqlite database containing"
        " legislator metadata. Otherwise add table to BILLS_DB."
    )
)
@click.option("--api_key", required=True, help="ProPublica Congress API Key.")
@click.option("--overwrite", is_flag=True)
@click.pass_context
@flow
def download(ctx, **args):
    """
    Retrieve metadata information from the ProPublica Congress API
    for every legislator in the bills database provided. Creates a new table
    in the bills database (or a new database, if --newdb).
    """

    dbpath = args['bills_db'] if not args['newdb'] else args['newdb']

    process_legislators(dbpath, args['api_key'], args['overwrite'])

