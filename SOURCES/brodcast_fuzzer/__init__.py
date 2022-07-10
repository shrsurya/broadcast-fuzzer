import click
from .brodcast_fuzzer import BrodcastFuzzer

@click.command()
@click.version_option()
@click.option('--dry', '-d',
              default=False,
              is_flag=True,
              help="Don't make changes, just print expected actions")
def cli(**kwargs):
    BrodcastFuzzer(**kwargs)