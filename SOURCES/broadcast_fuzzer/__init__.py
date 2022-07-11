import sys
import click
from .broadcast_fuzzer import BroadcastFuzzer

@click.command()
@click.version_option()
@click.option('--manifest', '-m',
              required=True,
              type=click.File('rb'),
              help="The path to manifest file, to be used")
@click.option('--dry', '-d',
              default=False,
              is_flag=True,
              help="Don't make changes, just print expected actions")
@click.option('--print','-p',
              default=False,
              is_flag=True,
              help="Print the manifest data")
def cli(**kwargs):
    BroadcastFuzzer(**kwargs)