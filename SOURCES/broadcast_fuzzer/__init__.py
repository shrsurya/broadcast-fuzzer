import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import click
from .broadcast_fuzzer import BroadcastFuzzer

@click.command()
@click.version_option()
@click.option("--manifest", "-m",
              required=True,
              type=click.File("rb"),
              help="The path to manifest file, to be used")
@click.option("--dry", "-d",
              default=False,
              is_flag=True,
              help="Don't make changes, just print expected actions")
@click.option("--print", "-p",
              default=False,
              is_flag=True,
              help="Print the manifest data")
@click.option("--data_runs", "-dr",
              default=10,
              help="Number of fuzzed files you want to create")
@click.option("--gen", "-g",
              default=False,
              is_flag=True,
              help="Generate Fuzzed data")
@click.option("--data_path", "-dp",
              default="FuzzedData/",
              help="Folder where you want the Fuzzed data")
@click.option("--seed_path", "-sp",
              default="SEED/",
              help="Path where you get Seed files")
@click.option("--adb_path", "-adb",
              help="Path to adb executable, required if ADB_PATH environment variable is not set")
@click.option("--execute", "-e",
              default=False,
              is_flag=True,
              help="Execute Intent Fuzzing")
def cli(**kwargs):
    BroadcastFuzzer(**kwargs)