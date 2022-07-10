import sys
import click
from .broadcast_fuzzer import broadcastFuzzer

@click.command()
@click.version_option()
# @click.option('--dry', '-d',
#               default=False,
#               is_flag=True,
#               help="Don't make changes, just print expected actions")
@click.option('--mainfest', '-m',
              default=False,
              is_flag=True,
              required=True,
              type=click.File('r+'),
              help="The path to manifest file, to be used")
# @click.option('--fuzz', '-f',
#               default=False,
#               is_flag=True,
#               help="Fuzz")
def cli(**kwargs):
    broadcastFuzzer(**kwargs)