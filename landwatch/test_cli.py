import os
import unittest
from .cli import cli_main

REQUIRED_MODULES = [
    m for m in next(os.walk(os.path.dirname(__file__)))[1]
    if not m.startswith('__')
]

class TestGenerateCLI(unittest.TestCase):
    def test_cli(self):
        self.assertTrue(
            set(REQUIRED_MODULES) == set(cli_main.commands.keys())
        )
