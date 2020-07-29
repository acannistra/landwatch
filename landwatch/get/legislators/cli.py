import click

from loguru import logger

from .legdb import LegislatorDB
from .legislators import get_sponsors

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
def download(ctx, **args):
    """
    Retrieve metadata information from the ProPublica Congress API
    for every legislator in the bills database provided. Creates a new table
    in the bills database (or a new database, if --newdb).
    """

    dbpath = args['bills_db'] if not args['newdb'] else args['newdb']

    legdb = LegislatorDB(dbpath, args['overwrite'])

    sponsors = get_sponsors(dbpath,args['api_key'])

    for sponsor, bills in sponsors:
        bills = bills.split(',')
        for bill in bills:

            legdb.write(sponsor, bill_id = bill, sponsor_type = 'sponsor')
