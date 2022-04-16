import click

from pythontools import common
from pythontools.iam import actdir


@click.command()
@click.argument('host', default=common.PC, help='the vm ip, on which to create the active directory')
def main(host):
    """
    \b
    This creates an active directory on the host mentioned, based on the specifications
    defined in pythontools.iam.ACTDIR_SPEC
    """
    actdir.create(host)

