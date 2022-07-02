import click
from prefect import flow
from prefect.task_runners import  SequentialTaskRunner
from loguru import logger

from .opensecrets import OSBulkData

@click.group(
    help="Get campaign finance data relevant to legislators"
    " of bills relevant to parcels."
)
@click.pass_context
def finance(ctx):
    pass

# @finance.command(
#     help="Download campaign finance data from OpenSecrets."
# )
# @click.argument("legislators")
# @click.argument("dest")
# @click.option(
#     "--type",
#     help="Type of data to download from OpenSecrets.",
#     type=click.Choice(DATA_TYPE_NAMES, case_sensitive=False)
# )
# @click.option(
#     "--api_key",
#     required=True,
#     help="OpenSecrets API Key."
# )
# @click.option(
#     "--cycle",
#     help="Election cycle to retrieve data for.",
#     default=2020,
#     show_default=True
# )
# def download(ctx, **args):
#     pass

@finance.command(
    'import',
    help="Import OpenData Bulk Data into sqlite database."
)
@click.option(
    "--register", help="Register flow with Prefect Cloud, don't run. Requires authentication."
)
@click.argument("bulkdatadir")
@click.argument("db")
@click.pass_context
@flow(task_runner=SequentialTaskRunner)
def _import(ctx, **args):
    print(ctx.parent.args)
    
    osb = OSBulkData(args['bulkdatadir'], args['db'])
    osb.load()
