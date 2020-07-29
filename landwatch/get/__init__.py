import os

import click
from importlib import import_module

from loguru import logger

SUBMODULES = [
    import_module(f".{m}", package='landwatch.get') for m in next(os.walk(os.path.dirname(__file__)))[1]
     if not m.startswith('__')
]
# Set up CLI group.
@click.group(name='get')
def get():
    pass

# Grab "_cli" for each module.
for sm in SUBMODULES:
    try:
        get.add_command(sm._cli)
    except AttributeError as e:
        logger.warning(e)

_cli = get
