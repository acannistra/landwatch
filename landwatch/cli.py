import os
from . import PACKAGE_NAME
from importlib import import_module

import click

# Check each module within `./landwatch`
SUBMODULES = [
    import_module(f".{m}", package='landwatch') for m in next(os.walk(os.path.dirname(__file__)))[1]
     if not m.startswith('__')
]
# Set up CLI group.
@click.group(name=PACKAGE_NAME)
def cli_main():
    pass

# Grab "_cli" for each module.
for sm in SUBMODULES:
    cli_main.add_command(sm._cli)
