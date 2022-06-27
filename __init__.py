import click
from .brodcast_fuzzer import BrodcastFuzzer

@click.command()
@click.version_option()
def cli(**kwargs):
    BrodcastFuzzer(**kwargs)