import sys
import click

from .bills import get_parcel_names, process_all_parcels
from .congress import ProPublicaAPI
from .billdb import BillDB

from loguru import logger

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
@click.option("--parcel_table", default="padus2_0fee", help="Tablename in lands sqlite database containing parcels", show_default=True)
@click.option("--parcel_col", default='unit_nm', help="Column in parcel sqlite database containing unique identifier names.", show_default=True)
@click.option("--api-key", help="ProPublica Congress API key.", required=True)
@click.option("--overwrite", help="Overwrite existing bills database", is_flag=True)
@click.option("--debug", is_flag=True)
@click.option("--parcels", metavar='<file>', help="File containing specific parcel names (ignores DB.) Useful for resuming failed parcels.")
@click.pass_context
def download(ctx, **args):
    """
    Creates an sqlite database at <dest> containing bills that are relevant
    to parcels in <lands>.
    """
    if not args['debug']:
        logger.remove()
        logger.add(sys.stderr, level='INFO')

    parcels = []
    if args['parcels']:
        logger.info(f"Reading parcels from file {args['parcels']}.")
        parcels = open(args['parcels']).read().splitlines()
    else:
        parcels = get_parcel_names(
            args['lands'],
            table_name = args['parcel_table'],
            col_name  = args['parcel_col'])

        logger.info(f"Found {len(parcels)} unique parcels in {args['parcel_table']}.{args['parcel_col']}")

    api = ProPublicaAPI(args['api_key'])
    db  = BillDB(args['dest'], overwrite=args['overwrite'], logger=logger)

    process_all_parcels(parcels, api, db)
