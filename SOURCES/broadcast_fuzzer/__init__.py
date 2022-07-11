import sys
import click
from .broadcast_fuzzer import BroadcastFuzzer

@click.command()
@click.version_option()
@click.option('--manifest', '-m',
              required=True,
              type=click.File('rb'),
              help="The path to manifest file, to be used")
def cli(**kwargs):
    BroadcastFuzzer(**kwargs)