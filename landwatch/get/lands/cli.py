import click
from .usgs import USGSProtectedLands
from .wdpa import WDPA


@click.group(
    help= "Download public lands data. Currently supports USGS and WDPA data (specify as TYPE positional argument).")
@click.argument("type")
@click.pass_context
def lands(ctx, type):
    ctx.ensure_object(dict)
    ctx.obj['type'] = type


@lands.command(
    help = "Download public lands data."
)
# @click.argument("type")
# @click.argument("dest")
@click.pass_context
def download(ctx):
    """Download public lands data."""
    if ctx.obj['type'] == "usgs":
        _data = USGSProtectedLands()
    if ctx.obj['type'] == "wdpa":
        _data = WDPA()
    else:
        raise click.UsageError(f"Data type \"{ctx.obj['type']}\" is not supported.")
    _data.download(dest)

@lands.command(help="Unzip already-downloaded data")
@click.argument("data")
@click.argument("dest")
@click.pass_context
def unzip(ctx, data, dest):
    if  ctx.obj['type'] == "usgs":
        _data = USGSProtectedLands(local_loc=data)
    if  ctx.obj['type'] == 'wdpa':
        _data = WDPA(local_loc=data)
    else:
        click.UsageError(f"Data type \"{ctx.obj['type']}\" is not supported.")

    _data.unzip(dest)
